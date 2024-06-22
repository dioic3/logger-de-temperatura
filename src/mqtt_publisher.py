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
    return round(random.uniform(20.0, 30.0), 2)

# Função para publicar temperatura
def publicar_temperatura(client):
    temperatura = ler_temperatura()
    dados = {
        "temperatura": temperatura,
        "timestamp": time.time()
    }
    client.publish(MQTT_TOPIC, json.dumps(dados))
    print(f"Publicado: {dados}")

# Configuração do cliente MQTT
client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)

client.loop_start()

try:
    while True:
        publicar_temperatura(client)
        time.sleep(5)  # Publica a cada 5 segundos
except KeyboardInterrupt:
    pass

client.loop_stop()
client.disconnect()
