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

    def receive_from(self, user_id: int):
        self.received.append(user_id)

    def send_to(self, user_id: int):
        self.sent.append(user_id)

    def unreceive_from(self, user_id: int):
        self.received.remove(user_id)

    def unsend_to(self, user_id: int):
        self.sent.remove(user_id)
