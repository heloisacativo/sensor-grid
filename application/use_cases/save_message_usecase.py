from domain.message import Message
from application.ports.message_repository import IMessageRepository

class SaveMessageUseCase:
    def __init__(self, repository: IMessageRepository):
        self.repository = repository

    def execute(self, topic: str, payload: str) -> Message:
        message = Message(topic=topic, payload=payload)

        is_critical = message.is_temperature and float(message.payload) > 100.0
        message.is_critical = is_critical

        # salva independente de onde vai salvar
        self.repository.save(message, is_critical)
        return message
