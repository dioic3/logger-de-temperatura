import paho.mqtt.client as mqtt
import time
import random
import json

# Configurações MQTT
MQTT_BROKER = "mqtt.eclipseprojects.io"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/temperatura"

# Função para simular leitura de temperatura
def ler_temperatura():
    return round(random.uniform(20.0, 40.0), 2)  # Simula temperaturas entre 20.0 °C e 40.0 °C

# Função para publicar temperatura de múltiplos sensores
def publicar_temperatura(client, sensor_id):
    temperatura = ler_temperatura()
    dados = {
        "sensor_id": sensor_id,
        "temperatura": temperatura,
        "timestamp": time.time()
    }
    client.publish(MQTT_TOPIC, json.dumps(dados))
    print(f"Publicado pelo sensor {sensor_id}: {dados}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_start()

try:
    sensor_ids = [1, 2, 3]  # IDs dos sensores simulados
    while True:
        for sensor_id in sensor_ids:
            publicar_temperatura(client, sensor_id)
            time.sleep(5)  # Publica a cada 5 segundos por sensor
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
