from dataclasses import dataclass

from eagxf.constants import NOT_ALNUM, QUESTION_NAMES
from eagxf.enums.property import Property


@dataclass
class Questions:
    about_me: str = "?"
    can_help: str = "?"
    need_help: str = "?"
    concerns: str = "?"

    @staticmethod
    def from_dict(questions: dict[str, str]) -> "Questions":
        return Questions(**questions)

    def to_dict(self) -> dict[str, str]:
        return self.__dict__

    def is_complete(self) -> bool:
        return all(question not in ("?", "") for question in self.__dict__.values())

    def __getitem__(self, key: str) -> str:
        return self.__dict__[key]

    def __setitem__(self, key: str, value: str) -> None:
        self.__dict__[key] = value

    def set_property(self, prop: Property, value: str) -> None:
        self[prop.low] = value

    def get_score(self, other: "Questions") -> int:
        return sum(
            NOT_ALNUM.sub("", kw.strip().lower()) in other[q_id.low].lower()
            for q_id in QUESTION_NAMES
            for kw in self[q_id.low].split(" ")
        )
