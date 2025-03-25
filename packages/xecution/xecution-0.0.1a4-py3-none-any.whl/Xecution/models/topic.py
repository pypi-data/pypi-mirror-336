from dataclasses import dataclass
from xecution.common.enums import KlineType

@dataclass(frozen=True)  # ✅ Makes the dataclass immutable and hashable
class KlineTopic:
    klineType: KlineType
    symbol: str
    timeframe: str