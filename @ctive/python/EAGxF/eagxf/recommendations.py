from dataclasses import dataclass, field
from typing import Any


@dataclass
class Recommendation:
    sender: int
    receiver: int
    person: int
    message: str

    @staticmethod
    def from_dict(data: dict[str, Any]) -> "Recommendation":
        return Recommendation(
            sender=data["sender"],
            receiver=data["receiver"],
            person=data["person"],
            message=data["message"],
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "sender": self.sender,
            "receiver": self.receiver,
            "person": self.person,
            "message": self.message,
        }

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Recommendation):
            return False
        return (
            self.sender == other.sender
            and self.receiver == other.receiver
            and self.person == other.person
        )

    def __hash__(self) -> int:
        return hash((self.sender, self.receiver, self.person))


@dataclass
class Recommendations:
    recommendations: list[Recommendation] = field(default_factory=list)

    def add(self, recommendation: Recommendation) -> None:
        self.recommendations.append(recommendation)

    def remove(self, recommendation: Recommendation) -> None:
        self.recommendations.remove(recommendation)

    def sent(self, sender: int) -> list[Recommendation]:
        return [
            recommendation
            for recommendation in self.recommendations
            if recommendation.sender == sender
        ]

    def received(self, receiver: int) -> list[Recommendation]:
        return [
            recommendation
            for recommendation in self.recommendations
            if recommendation.receiver == receiver
        ]

    def to_dict(self) -> list[dict[str, Any]]:
        return [recommendation.to_dict() for recommendation in self.recommendations]

    @staticmethod
    def from_dict(data: list[dict[str, Any]]) -> "Recommendations":
        return Recommendations(
            recommendations=[
                Recommendation.from_dict(recommendation) for recommendation in data
            ]
        )

    def remove_by_sender_and_receiver(self, sender: int, receiver: int) -> None:
        self.recommendations = [
            recommendation
            for recommendation in self.recommendations
            if not (
                recommendation.sender == sender and recommendation.receiver == receiver
            )
        ]
