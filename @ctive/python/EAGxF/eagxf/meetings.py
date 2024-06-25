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


@dataclass
class Meetings:
    upcoming: list[Meeting] = field(default_factory=list)
    past: list[Meeting] = field(default_factory=list)
    ongoing: Meeting | None = None

    def to_dict(self) -> dict[str, list[dict[str, int | str]]]:
        return {
            "future": [meeting.to_dict() for meeting in self.upcoming],
            "past": [meeting.to_dict() for meeting in self.past],
        }

    @staticmethod
    def from_dict(data: dict[str, list[dict[str, Any]]]) -> "Meetings":
        upcoming = [
            Meeting(m["partner_id"], Date.from_str(m["date"])) for m in data["future"]
        ]
        past = [
            Meeting(m["partner_id"], Date.from_str(m["date"])) for m in data["past"]
        ]
        return Meetings(upcoming, past)
    
    def request_meeting(self, partner_id: int, date: Date) -> None:
        self.upcoming.append(Meeting(partner_id, date))

    def request_video_call(self, partner_id: int) -> None:
        self.upcoming.append(Meeting(partner_id))

    def cancel_meeting_with(self, partner_id: int) -> None:
        self.upcoming = [
            meeting for meeting in self.upcoming if meeting.partner_id != partner_id
        ]
