from abc import ABC, abstractmethod
from domain.message import Message

class IMessageRepository(ABC):
    @abstractmethod
    def save(self, message: Message, is_critical: bool) -> Message:
        pass
