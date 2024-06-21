import paho.mqtt.client as mqtt
import json

# Configurações MQTT
MQTT_BROKER = "mqtt.eclipseprojects.io"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/temperatura"
LOG_FILE = "temperatura_log.txt"

# Callback quando uma mensagem é recebida
def on_message(client, userdata, message):
    dados = json.loads(message.payload.decode())
    with open(LOG_FILE, "a") as log:
        log.write(f"{dados['timestamp']}: {dados['temperatura']}C\n")
    print(f"Registrado: {dados}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.subscribe(MQTT_TOPIC)
client.on_message = on_message

client.loop_forever()
