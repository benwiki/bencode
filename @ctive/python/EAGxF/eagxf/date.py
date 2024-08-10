from datetime import datetime

from eagxf.constants import DATE_FORMAT


class Date(datetime):
    def is_future(self) -> bool:
        return self >= Date.current()

    def is_past(self) -> bool:
        return self < Date.current()

    @staticmethod
    def is_valid(date: str) -> bool:
        valid_format = bool(DATE_FORMAT.fullmatch(date))
        if not valid_format:
            return False
        try:
            Date.from_str(date)
        except ValueError:
            return False
        return True
    
    @staticmethod
    def valid_future_date(date: str) -> bool:
        if not Date.is_valid(date):
            return False
        return Date.from_str(date).is_future()
    
    @staticmethod
    def valid_past_date(date: str) -> bool:
        if not Date.is_valid(date):
            return False
        return Date.from_str(date).is_past()

    @staticmethod
    def from_str(date_str: str) -> "Date":
        date_str = date_str.strip()
        if " " not in date_str:
            d, m, y = map(int, date_str.split("."))
            return Date(y, m, d)

        dmy, hms = date_str.split(" ")
        if hms.count(":") == 1:
            hms += ":00"
        d, m, y = map(int, dmy.split("."))
        h, mi, s = map(int, hms.split(":"))
        return Date(y, m, d, h, mi, s)

    def __str__(self) -> str:
        return self.strftime(r"%d.%m.%Y %H:%M")

    def __repr__(self) -> str:
        y, m, d = self.year, self.month, self.day
        h, mi, s = self.hour, self.minute, self.second
        return f"Date({y=}, {m=}, {d=}, {h=}, {mi=}, {s=})"

    @staticmethod
    def default() -> "Date":
        return Date(1, 1, 1900)

    @staticmethod
    def from_datetime(dt: datetime) -> "Date":
        return Date(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

    @staticmethod
    def current() -> "Date":
        return Date.from_datetime(datetime.now())
