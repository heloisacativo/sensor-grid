import os

import paho.mqtt.client as mqtt
from infrastructure.mqtt.handler import ao_conectar, ao_receber_mensagem, initialize
from application.use_cases.save_message_usecase import SaveMessageUseCase

try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:
    pass

MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = os.getenv("MQTT_PORT")
MQTT_CLIENT_ID = os.getenv("MQTT_CLIENT_ID")

if not MQTT_HOST or not MQTT_PORT or not MQTT_CLIENT_ID:
    raise EnvironmentError(
        "MQTT_HOST, MQTT_PORT e MQTT_CLIENT_ID devem estar definidos no .env ou variáveis de ambiente"
    )

try:
    MQTT_PORT = int(MQTT_PORT)
except ValueError:
    raise ValueError("MQTT_PORT deve ser um número inteiro")

mqtt_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, MQTT_CLIENT_ID)


def setup_mqtt(use_case: SaveMessageUseCase):
    initialize(use_case)
    mqtt_client.on_connect = ao_conectar
    mqtt_client.on_message = ao_receber_mensagem


def start_mqtt():
    mqtt_client.connect(MQTT_HOST, MQTT_PORT)
    mqtt_client.loop_start()
    print(f"✅ BACKEND CONECTADO VIA MQTT: {MQTT_HOST}:{MQTT_PORT}")


def stop_mqtt():
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
