from dataclasses import dataclass, field
from typing import Any

from eagxf.date import Date


@dataclass
class Meeting:
    partner_id: int
    date: Date = field(default_factory=Date.default)

    @property
    def time_bound(self) -> bool:
        return self.date != Date.default()

    def to_dict(self) -> dict[str, int | str]:
        return {
            "partner_id": self.partner_id,
            "date": str(self.date),
        }

    def is_future(self) -> bool:
        return self.date.is_future()

    def is_past(self) -> bool:
        return self.date.is_past()


@dataclass
class Meetings:
    future: list[Meeting] = field(default_factory=list)
    past: list[Meeting] = field(default_factory=list)
    ongoing: Meeting | None = None

    @property
    def all(self) -> list[Meeting]:
        return self.future + self.past

    def to_dict(self) -> dict[str, list[dict[str, int | str]]]:
        return {
            "future": [meeting.to_dict() for meeting in self.future],
            "past": [meeting.to_dict() for meeting in self.past],
        }

    @staticmethod
    def from_dict(data: dict[str, list[dict[str, Any]]]) -> "Meetings":
        future = [
            Meeting(m["partner_id"], Date.from_str(m["date"])) for m in data["future"]
        ]
        past = [
            Meeting(m["partner_id"], Date.from_str(m["date"])) for m in data["past"]
        ]
        not_future = [meeting for meeting in future if not meeting.is_future()]
        future = [meeting for meeting in future if not meeting in not_future]
        past.extend(not_future)
        return Meetings(future, past)

    def request(self, partner_id: int, date: Date) -> None:
        self.future.append(Meeting(partner_id, date))

    def cancel(self, partner_id: int, meeting: Meeting) -> None:
        if meeting in self.future:
            self.future.remove(meeting)
        elif meeting in self.past:
            self.past.remove(meeting)
        # self.future = [
        #     mtg
        #     for mtg in self.future
        #     if not (mtg.partner_id == partner_id and mtg.date == meeting.date)
        # ]
