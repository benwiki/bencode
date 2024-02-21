from dataclasses import dataclass


@dataclass
class Date:
    day: int
    month: int
    year: int
    hour: int | None = None
    minute: int | None = None
    second: int | None = None

    def __str__(self):
        if self.hour is not None:
            return (
                f"{self.day:02}.{self.month:02}.{self.year}"
                f" {self.hour:02}:{self.minute:02}:{self.second:02}"
            )
        return f"{self.day:02}.{self.month:02}.{self.year}"

    def __repr__(self):
        return str(self)