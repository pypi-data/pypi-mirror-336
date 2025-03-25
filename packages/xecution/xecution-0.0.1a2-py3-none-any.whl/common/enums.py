from enum import Enum

class KlineType(Enum):
    Binance_Spot = 1
    Binance_Futures = 2

class Mode(Enum):
    Live = 1
    Backtest = 2
    Testnet = 3
    
class ConcurrentRequest(Enum):
    Max = 3
    Chunk_Size = 5