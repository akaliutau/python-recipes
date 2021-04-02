from enum import Enum, unique


@unique
class ForecastType(Enum):
    TODAY = 'today'
    TENDAYS = 'tenday'
