import paho.mqtt.client as mqtt
import json
import time

# Configurações MQTT
MQTT_BROKER = "mqtt.eclipseprojects.io"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/temperatura"
LOG_FILE = "../logs/temperatura_log.txt"
ALERTA_LIMITE = 30  # Limite de temperatura para disparar alerta

# Callback quando uma mensagem é recebida
def on_message(client, userdata, message):
    dados = json.loads(message.payload.decode())
    sensor_id = dados.get('sensor_id')
    temperatura = dados.get('temperatura')
    timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dados['timestamp']))

    with open(LOG_FILE, "a") as log:
        log.write(f"Sensor {sensor_id} - {timestamp}: {temperatura}C\n")
    print(f"Registrado pelo sensor {sensor_id}: {dados}")

    if temperatura > ALERTA_LIMITE:
        enviar_alerta(sensor_id, temperatura, timestamp)

def enviar_alerta(sensor_id, temperatura, timestamp):
    alert_message = f"ALERTA! Sensor {sensor_id} detectou temperatura alta: {temperatura} °C em {timestamp}"
    print(alert_message)

# Configuração do cliente MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.subscribe(MQTT_TOPIC)
client.on_message = on_message

client.loop_forever()
