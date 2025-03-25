from dataclasses import dataclass
import datetime
from typing import Optional
from xecution.models.topic import KlineTopic
from xecution.common.enums import Mode

@dataclass
class RuntimeConfig:
    mode: Mode
    kline_topic: list[KlineTopic]
    datasource_topic: Optional[list[str]]
    start_time: datetime
    data_count: int
    API_Key: Optional[str]
    API_Secret: Optional[str]