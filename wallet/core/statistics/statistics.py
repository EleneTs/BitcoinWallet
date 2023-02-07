from dataclasses import dataclass, field
from http import HTTPStatus
from typing import Optional


@dataclass
class Response:
    message: str = ""
    status_code: int = HTTPStatus.OK


@dataclass
class StatisticsInfo:
    platform_profit: float = 0.0
    transactions_count: int = 0


@dataclass
class StatisticsResponse(Response):
    statistics_info: Optional[StatisticsInfo] = field(
        default_factory=lambda: StatisticsInfo()
    )
