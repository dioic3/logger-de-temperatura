import tkinter as tk
import tkinter.scrolledtext as scrolledtext
import threading
import time
import json
import paho.mqtt.client as mqtt

# Configurações MQTT
MQTT_BROKER = "mqtt.eclipseprojects.io"
MQTT_PORT = 1883
MQTT_TOPIC = "sensor/temperatura"
LOG_FILE = "../logs/temperatura_log.txt"
ALERTA_LIMITE = 30  # Limite de temperatura para disparar alerta

class TemperaturaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Logger de Temperatura")

        self.temperatura_label = tk.Label(root, text="Últimas Temperaturas:")
        self.temperatura_label.pack(pady=10)

        self.sensores_frame = tk.Frame(root)
        self.sensores_frame.pack()

        self.sensores = {}
        for sensor_id in range(1, 4):  # IDs dos sensores
            frame = tk.Frame(self.sensores_frame)
            frame.pack(pady=5)

            label = tk.Label(frame, text=f"Sensor {sensor_id}:")
            label.pack(side=tk.LEFT, padx=5)

            temp_var = tk.StringVar()
            temp_var.set("N/A")
            temp_display = tk.Label(frame, textvariable=temp_var, font=('Helvetica', 18))
            temp_display.pack(side=tk.LEFT, padx=5)

            self.sensores[sensor_id] = temp_var

        self.log_label = tk.Label(root, text="Log de Temperaturas:")
        self.log_label.pack(pady=10)

        self.log_text = scrolledtext.ScrolledText(root, width=50, height=10)
        self.log_text.pack()

        self.alerta_label = tk.Label(root, text="", fg="red")
        self.alerta_label.pack(pady=10)

        self.iniciar_btn = tk.Button(root, text="Iniciar Logger", command=self.iniciar_logger)
        self.iniciar_btn.pack(pady=10)

        self.parar_btn = tk.Button(root, text="Parar Logger", command=self.parar_logger, state=tk.DISABLED)
        self.parar_btn.pack(pady=5)

        self.client = mqtt.Client()
        self.client.connect(MQTT_BROKER, MQTT_PORT, 60)
        self.client.on_message = self.on_message
        self.client.subscribe(MQTT_TOPIC)

        self.logger_ativo = False
        self.log_file = open(LOG_FILE, "a")

    def iniciar_logger(self):
        self.logger_ativo = True
        self.iniciar_btn.config(state=tk.DISABLED)
        self.parar_btn.config(state=tk.NORMAL)
        threading.Thread(target=self.receive_messages).start()

    def parar_logger(self):
        self.logger_ativo = False
        self.iniciar_btn.config(state=tk.NORMAL)
        self.parar_btn.config(state=tk.DISABLED)

    def receive_messages(self):
        while self.logger_ativo:
            self.client.loop()
            time.sleep(0.1)

    def on_message(self, client, userdata, message):
        dados = json.loads(message.payload.decode())
        sensor_id = dados['sensor_id']
        temperatura = dados['temperatura']
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dados['timestamp']))

        # Atualiza o texto da temperatura do sensor correspondente
        if sensor_id in self.sensores:
            if temperatura > ALERTA_LIMITE:
                self.sensores[sensor_id].set(f"{temperatura} °C (ALERTA!)")
                self.mostrar_alerta(f"ALERTA! Sensor {sensor_id} detectou temperatura alta: {temperatura} °C")
            else:
                self.sensores[sensor_id].set(f"{temperatura} °C")

        self.log_text.insert(tk.END, f"Sensor {sensor_id} - {timestamp}: {temperatura} °C\n")
        self.log_text.see(tk.END)
        
        self.log_file.write(f"Sensor {sensor_id} - {timestamp}: {temperatura} °C\n")
        self.log_file.flush()

    def mostrar_alerta(self, mensagem):
        self.alerta_label.config(text=mensagem)

    def fechar_janela(self):
        self.log_file.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TemperaturaApp(root)
    root.protocol("WM_DELETE_WINDOW", app.fechar_janela)
    root.mainloop()
