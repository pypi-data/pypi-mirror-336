import asyncio
import numpy as np
import asyncio
import logging
from datetime import datetime, timezone
from xecution.common.enums import KlineType
from xecution.models.config import RuntimeConfig, KlineTopic, Mode
from xecution.services.exchange.binance_service import BinanceService

# Enable logging to see real-time data
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class BaseEngine:
    """Base engine that initializes BinanceService and processes on_candle_closed and on_datasource_update."""

    def __init__(self, config: RuntimeConfig):
        self.config = config
        self.data_map = {}  # Local data storage for kline data
        self.binance_service = BinanceService(config, self.data_map)  # Pass data_map to BinanceService

    async def on_candle_closed(self, kline_topic: KlineTopic):
        """Handles closed candle data using `self.data_map[kline_topic]`."""
        
        # Ensure kline_topic exists in data_map
        if kline_topic not in self.data_map:
            logging.error(f"No candle data found for {kline_topic}")
            return
        
        # Access stored candle data
        candles = self.data_map[kline_topic]
        start_time = np.array([float(c["start_time"]) for c in candles])
        close = np.array([float(c["close"]) for c in candles])
        
        logging.info(
            f"Last Kline Closed | {kline_topic.symbol}-{kline_topic.timeframe} | Close: {close[-1]} | Time: {datetime.fromtimestamp(start_time[-1] / 1000)}"
        )

    async def on_datasource_update(self, datasource_topic):
        """Handles updates from external data sources."""
        logging.info(f"Datasource Updated | Topic: {datasource_topic}")

    async def start(self):
        """Starts BinanceService and behaves differently based on the runtime mode."""
        await self.binance_service.get_klines(self.on_candle_closed)

        if self.config.mode == Mode.Live:
            while True:
                await asyncio.sleep(1)  # Keep the loop alive
        else:
            logging.info("Backtest mode completed. Exiting.")

if __name__ == "__main__":
    engine = BaseEngine(
        RuntimeConfig(
            mode= Mode.Live,
            kline_topic=[
                KlineTopic(klineType=KlineType.Binance_Futures, symbol="BTCUSDT", timeframe="1m"),
                KlineTopic(klineType=KlineType.Binance_Futures, symbol="ETHUSDT", timeframe="1m"),
            ],
            datasource_topic=None,
            start_time=datetime(2025,3,22,0,0,0,tzinfo=timezone.utc),
            data_count=3000,
            API_Key=None,  # Replace with your API Key if needed
            API_Secret=None  # Replace with your API Secret if needed
        )
    )

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(engine.start())  # will exit automatically for backtest
    except KeyboardInterrupt:
        logging.info("Shutting down BinanceService...")
    finally:
        loop.close()

