from pydantic import BaseModel, Field

class MessagePayloadDTO(BaseModel):
    topic: str = Field(..., min_length=1, description="O tópico MQTT")
    payload: str = Field(..., description="O valor lido pelo sensor")

class SimulatorAdapter:
    @staticmethod
    def parse_raw_data(raw_string: str) -> MessagePayloadDTO:
        parts = raw_string.split("|")
        if len(parts) == 3:
            return MessagePayloadDTO(
                topic=f"maquina/{parts[0]}/{parts[1].lower()}",
                payload=parts[2]
            )
        raise ValueError("Formato de protocolo desconhecido")