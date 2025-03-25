import logging
from xecution.models.config import RuntimeConfig
from xecution.models.topic import KlineTopic
from xecution.services.connection.websockets import WebSocketService
from xecution.services.exchange.binance_helper import BinanceHelper
from xecution.common.enums import Mode

class BinanceService:
    
    def __init__(self, config: RuntimeConfig, data_map: dict):
        """
        Binance Service for managing WebSocket and API interactions.
        """
        self.config = config
        self.ws_service = WebSocketService()
        self.data_map = data_map  # External data map reference
    
    async def get_klines(self, on_candle_closed):
        """
        呼叫 Binance /api/v3/klines 取得 K 線
        """
        try:
            for kline_topic in self.config.kline_topic :
                binance_helper = BinanceHelper(self.config, kline_topic)
                if self.config.mode == Mode.Backtest:
                    candles = await binance_helper.getKlineRestAPI(on_candle_closed)
                    self.data_map[kline_topic] = candles
                    await on_candle_closed(kline_topic)
                
                elif self.config.mode == Mode.Live:
                    await self.listen_kline(on_candle_closed,kline_topic,binance_helper)
        except Exception as e:
            logging.error(f"[BinanceService] get_klines failed: {e}")


    def place_order(self, symbol="BTCUSDT", side="BUY", quantity=0.01, price=None, order_type="LIMIT"):
        """
        下單 (私有API)
        """
        endpoint = "/v3/order"
        params = {
            "symbol": symbol,
            "side": side.upper(),
            "type": order_type.upper(),
            "quantity": quantity,
        }
        if price and order_type.upper() == "LIMIT":
            params["price"] = price
            # timeInForce 對 BINANCE LIMIT ORDER 通常可 GTC、IOC等
            params["timeInForce"] = "GTC"

        # 私有API => auth=True 需簽名
        resp = self.client.request("POST", endpoint, params=params, auth=True)
        return resp

    async def listen_kline(self, on_candle_closed, kline_topic: KlineTopic, binance_helper: BinanceHelper):
        """Subscribe to Binance WebSockets, receive messages, and send closed candles to `on_candle_closed`."""
        try:
            def get_connection_urls():
                """Generate WebSocket connection URLs using `RuntimeConfig.kline_topic`."""
                try:
                    connection_urls = {}
                    kline_topic_mapping = {}  # Store kline_topic info for mapping
                    
                    ws_url = binance_helper.get_websocket_base_url(kline_topic) + f"/{kline_topic.symbol.lower()}@kline_{kline_topic.timeframe.lower()}"

                    connection_urls[ws_url] = (ws_url, None)  # No extra subscription message needed
                    kline_topic_mapping[ws_url] = kline_topic  # Maps WebSocket URL to kline_topic
                    
                    # Ensure external data_map stores kline_topic keys
                    self.data_map[kline_topic] = []

                    return connection_urls, kline_topic_mapping
                except Exception as e:
                    logging.error(f"[BinanceService] get_connection_urls failed: {e}")

            async def message_handler(exchange, message):
                """Processes incoming kline messages and calls `on_candle_closed` with `kline_topic` only."""
                try:
                    kline = message.get("k", {})
                    if not kline:
                        return  # Ignore invalid messages

                    is_closed = kline.get("x", False)  # Ensure candle is fully closed
                    if not is_closed:
                        return  # Skip unfinished candles

                    # Extract kline_topic from mapping
                    ws_url = message.get("s")  # Get symbol from message
                    kline_topic = next((kt for kt in self.config.kline_topic if ws_url == kt.symbol), None)
                    if not kline_topic:
                        logging.warning(f"[BinanceService][{exchange}] Kline topic mapping not found for {ws_url}. Skipping message.")
                        return
                    
                    # call get_kline_restapi
                    candles = await binance_helper.getKlineRestAPI(on_candle_closed)
                    
                    # compare the last candles with kline if same data then return the candles to on_candle_closed
                    if len(candles) > 0 :
                        last_candle = candles[-1]
                        logging.debug(f"last_candle {last_candle}")
                        logging.debug(f"kline { binance_helper.convert_ws_kline(kline)}")
                        if last_candle["start_time"] == binance_helper.convert_ws_kline(kline).get("start_time"):
                            # append candles to data_map
                            self.data_map[kline_topic] = candles

                    logging.debug(f"[{exchange}] Candle Closed | {kline_topic.symbol}-{kline_topic.timeframe} | Close: {kline.get('c')}")

                    # Only pass `kline_topic` to `on_candle_closed`
                    await on_candle_closed(kline_topic)
                except Exception as e:
                    logging.error(f"[BinanceService] message_handler failed: {e}")

            # Establish WebSocket connections
            connection_urls, kline_topic_mapping = get_connection_urls()
            for exchange_name, (ws_url, subscription_message) in connection_urls.items():
                logging.debug(f"Connecting to {ws_url}")
                await self.ws_service.subscribe(exchange_name, ws_url, subscription_message, message_handler)

            logging.info("[BinanceService] WebSocket connections initialized.")
        except Exception as e:
            logging.error(f"[BinanceService] listen_kline failed: {e}")
