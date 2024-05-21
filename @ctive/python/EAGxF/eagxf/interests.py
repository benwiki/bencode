from dataclasses import dataclass, field


@dataclass
class Interests:
    sent: list[int] = field(default_factory=list)
    received: list[int] = field(default_factory=list)

    @staticmethod
    def from_dict(data: dict[str, list[int]]) -> "Interests":
        return Interests(sent=data["sent"], received=data["received"])
    
    def to_dict(self) -> dict[str, list[int]]:
        return {"sent": self.sent, "received": self.received}
