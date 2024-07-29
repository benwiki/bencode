from dataclasses import dataclass

from eagxf.constants import NOT_ALPHANUMERIC, Q_MAPPING, QUESTION_NAMES
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

    def __getitem__(self, prop: Property) -> str:
        return self.__dict__[prop.to_str]

    def __setitem__(self, prop: Property, value: str) -> None:
        self.__dict__[prop.to_str] = value

    def set(self, prop: Property, value: str) -> None:
        self[prop] = value

    def get_score(self, other: "Questions") -> int:
        with open("stopwords.txt", "r", encoding="utf-8") as f:
            stopwords = set(f.read().splitlines())
        return sum(  # type: ignore
            (  # type: ignore
                (1.0 if q_id2 == Q_MAPPING[q_id1] else 0.5)
                if kw in other[q_id2].lower()
                else 0.0
            )
            for q_id1 in QUESTION_NAMES
            for q_id2 in QUESTION_NAMES
            for kw in NOT_ALPHANUMERIC.split(self[q_id1].lower())
            if kw not in stopwords
        )
