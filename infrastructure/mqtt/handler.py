import asyncio
from domain.message import Message
from application.use_cases.save_message_usecase import SaveMessageUseCase
from infrastructure.ws.broadcaster import broadcast_event

save_message_use_case: SaveMessageUseCase | None = None

def initialize(use_case: SaveMessageUseCase):
    global save_message_use_case
    save_message_use_case = use_case


def ao_conectar(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("\nCONECTADO AO MOSQUITTO COM SUCESSO!")
        client.subscribe("maquina/#")
        print("Escutando telemetria industrial (maquina/#)...")
    else:
        print(f"Falha ao conectar. Código: {reason_code}")


def ao_receber_mensagem(client, userdata, msg):
    if save_message_use_case is None:
        raise RuntimeError("SaveMessageUseCase não inicializado")

    print(f"\nEVENTO DETECTADO no tópico: {msg.topic}")

    try:
        payload = msg.payload.decode()
        print(f"Valor recebido: {payload}°C")

        message = Message(topic=msg.topic, payload=payload)
        saved_message = save_message_use_case.execute(message.topic, message.payload)

        status = "CRÍTICO" if saved_message.is_critical else "NORMAL"
        print(
            "🚨 ALERTA CRÍTICO: Temperatura acima do limite! Risco de Downtime."
            if saved_message.is_critical
            else "Status: Operação dentro da normalidade."
        )

        print(f"Evento registrado no SQLite: {saved_message.topic} = {saved_message.payload}°C")

        coro_event = {
            "topico": saved_message.topic,
            "valor": float(saved_message.payload),
            "status": status,
            "classe": "text-rose-400" if saved_message.is_critical else "text-emerald-400",
            "data_hora": saved_message.timestamp.isoformat(),
        }

        asyncio.run_coroutine_threadsafe(broadcast_event(coro_event), asyncio.get_event_loop())

    except Exception as e:
        print(f"Erro ao processar mensagem: {e}")

    print("-" * 50)
