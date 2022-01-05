from datetime import date, datetime

from dateutil import parser


def to_datetime(value: str) -> datetime:
    return parser.parse(value)


def to_iso(value: datetime) -> str:
    return value.isoformat()


def to_date(value: str) -> str:
    return date.isoformat(parser.parse(value))


def timestamp() -> str:
    return datetime.now().isoformat()
