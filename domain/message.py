from datetime import datetime
from dataclasses import dataclass, field

@dataclass
class Message:
    topic: str
    payload: str
    timestamp: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        if not self.topic or not self.topic.strip():
            raise ValueError("O tópico não pode ser vazio.")

    @property
    def is_temperature(self) -> bool:
        return "temp" in self.topic.lower()