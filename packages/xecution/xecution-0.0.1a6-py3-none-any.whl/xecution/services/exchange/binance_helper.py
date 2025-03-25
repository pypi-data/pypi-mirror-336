import logging
import aiohttp
import math
from datetime import datetime, timezone
from xecution.common.enums import KlineType, Mode
from xecution.common.exchange.live_constants import LiveConstants
from xecution.models.config import RuntimeConfig
from xecution.models.topic import KlineTopic
from .safe_kline_downloader import SafeKlineDownloader

# 處理binance service的小功能
class BinanceHelper:
    def __init__(self, config: RuntimeConfig, kline_topic: KlineTopic):
        self.config = config
        self.kline_topic = kline_topic
        self.base_url = self.get_restapi_base_url(kline_topic)
        
    # 取得 interval 對應的毫秒值
    interval_to_ms = {
        "1m": 60 * 1000,
        "3m": 3 * 60 * 1000,
        "5m": 5 * 60 * 1000,
        "15m": 15 * 60 * 1000,
        "30m": 30 * 60 * 1000,
        "1h": 60 * 60 * 1000,
        "2h": 2 * 60 * 60 * 1000,
        "4h": 4 * 60 * 60 * 1000,
        "6h": 6 * 60 * 60 * 1000,
        "8h": 8 * 60 * 60 * 1000,
        "12h": 12 * 60 * 60 * 1000,
        "1d": 24 * 60 * 60 * 1000,
    }
    
    @staticmethod
    def convert_ws_kline(k: dict) -> dict:
        """
        Convert Binance WebSocket kline message to simplified format.
        """
        try:
            return {
                "start_time": int(k.get("t")),
                "open": float(k.get("o")),
                "high": float(k.get("h")),
                "low": float(k.get("l")),
                "close": float(k.get("c")),
                "volume": float(k.get("v"))
            }
        except Exception as e:
            logging.exception(f"Failed to convert WebSocket kline: {k}")
            return {}

    @staticmethod
    def convert_rest_kline(kline: list) -> dict:
        """
        Convert Binance REST API kline to simplified format.
        """
        try:
            return {
                "start_time": kline[0],
                "open": float(kline[1]),
                "high": float(kline[2]),
                "low": float(kline[3]),
                "close": float(kline[4]),
                "volume": float(kline[5])
            }
        except Exception as e:
            logging.exception(f"Failed to convert REST kline: {kline}")
            return {}
    
    @staticmethod
    def get_restapi_base_url(kline_topic: KlineTopic):
        """
        根據 KlineType 決定使用的 REST API base URL
        """
        kline_type = kline_topic.klineType
        if kline_type == KlineType.Binance_Spot:
            return LiveConstants.Binance.RESTAPI_SPOT_URL
        elif kline_type == KlineType.Binance_Futures:
            return LiveConstants.Binance.RESTAPI_FUTURES_URL
        raise ValueError("Unsupported KlineType")
    
    @staticmethod
    def get_websocket_base_url(kline_topic: KlineTopic):
        """
        根據 KlineType 決定使用的 WebSocket base URL
        """
        kline_type = kline_topic.klineType
        if kline_type == KlineType.Binance_Spot:
            return LiveConstants.Binance.WEBSOCKET_SPOT_URL
        elif kline_type == KlineType.Binance_Futures:
            return LiveConstants.Binance.WEBSOCKET_FUTURES_URL
        raise ValueError("Unsupported KlineType")
    
    async def fetch_kline(self,session, url, params):
        async with session.get(url, params=params) as response:
            return await response.json()  
        
    async def getKlineRestAPI(self, on_candle_closed):
        try:
            endpoint = self.base_url + ("/v3/klines" if self.kline_topic.klineType == KlineType.Binance_Spot else  "/v1/klines")
            symbol = self.kline_topic.symbol
            interval = self.kline_topic.timeframe.lower()

            total_data = []
            async with aiohttp.ClientSession() as session:
                if self.config.mode == Mode.Backtest:
                    # 計算起始時間與現在 UTC 的毫秒時間
                    start_time = int(self.config.start_time.timestamp() * 1000)
                    now_ms = int(datetime.now(timezone.utc).timestamp() * 1000)

                    # 計算所需資料筆數
                    time_increment = self.interval_to_ms.get(interval, 60 * 1000)
                    total_candles_expected = math.ceil((now_ms - start_time) / time_increment)
                    logging.debug(f"symbol: {symbol}, interval: {interval}, 預計抓取 {total_candles_expected} 筆 K 線資料")

                    # 使用 SafeKlineDownloader（和 Live 模式共用）
                    downloader = SafeKlineDownloader(
                        session=session,
                        fetch_func=self.fetch_kline,
                        endpoint=endpoint,
                        symbol=symbol,
                        interval=interval,
                        max_limit=1000,  # Spot REST API 限制
                        time_increment_ms=time_increment,
                        max_concurrent_requests=5,
                        chunk_sleep=0.5
                    )
                    total_data = await downloader.download(start_time=start_time, total_needed=total_candles_expected)

                    # 轉換格式
                    converted_data = [self.convert_rest_kline(k) for k in total_data]
                    return converted_data

                elif self.config.mode == Mode.Live:
                    total_needed = self.config.data_count
                    time_increment = BinanceHelper.interval_to_ms.get(interval, 60 * 1000)
                    start_time = None

                    downloader = SafeKlineDownloader(
                        session=session,
                        fetch_func=self.fetch_kline,
                        endpoint=endpoint,
                        symbol=symbol,
                        interval=interval,
                        max_limit=1000,
                        time_increment_ms=time_increment,
                        max_concurrent_requests=3,
                        chunk_sleep=0.5
                    )

                    total_data = await downloader.download_reverse(total_needed=total_needed)
                    converted_data = [self.convert_rest_kline(k) for k in total_data]
                    return converted_data
                else:
                    raise ValueError(f"Unsupported mode: {self.config.mode}")
        except Exception as e:
            logging.error(f"getKlineRestAPI: {e}")
