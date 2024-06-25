import datetime
from dataclasses import dataclass

from eagxf.constants import DATE_FORMAT


@dataclass
class Date:
    day: int
    month: int
    year: int
    hour: int | None = None
    minute: int | None = None
    second: int | None = None

    def __str__(self) -> str:
        dmy = f"{self.day:02}.{self.month:02}.{self.year}"
        if self.hour is not None:
            return f"{dmy} {self.hour:02}:{self.minute:02}:{self.second:02}"
        return dmy

    def __repr__(self) -> str:
        return str(self)

    @staticmethod
    def is_valid(date: str) -> bool:
        return bool(DATE_FORMAT.fullmatch(date))

    @staticmethod
    def from_str(date_str: str) -> "Date":
        date_str = date_str.strip()
        if " " in date_str:
            dmy, hms = date_str.split(" ")
            if hms.count(":") == 1:
                hms += ":00"
            return Date(*map(int, dmy.split(".") + hms.split(":")))
        return Date(*map(int, date_str.split(".")))

    @staticmethod
    def default() -> "Date":
        return Date(1, 1, 2000)

    @staticmethod
    def current() -> "Date":
        current = datetime.datetime.now()
        return Date(
            day=current.day,
            month=current.month,
            year=current.year,
            hour=current.hour,
            minute=current.minute,
            second=current.second,
        )
