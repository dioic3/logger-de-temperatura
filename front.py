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
LOG_FILE = "temperatura_log.txt"

class TemperaturaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Logger de Temperatura")

        self.temperatura_label = tk.Label(root, text="Última Temperatura:")
        self.temperatura_label.pack(pady=10)

        self.temperatura_atual = tk.StringVar()
        self.temperatura_atual.set("N/A")
        self.temperatura_display = tk.Label(root, textvariable=self.temperatura_atual, font=('Helvetica', 24))
        self.temperatura_display.pack()

        self.log_label = tk.Label(root, text="Log de Temperaturas:")
        self.log_label.pack(pady=10)

        self.log_text = scrolledtext.ScrolledText(root, width=50, height=10)
        self.log_text.pack()

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
        temperatura = dados['temperatura']
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(dados['timestamp']))

        # Atualiza o texto da temperatura com a cor correspondente
        if temperatura > 25:
            self.temperatura_display.config(fg='green')
        else:
            self.temperatura_display.config(fg='red')
        
        self.temperatura_atual.set(f"{temperatura} °C")
        self.log_text.insert(tk.END, f"{timestamp}: {temperatura} °C\n")
        self.log_text.see(tk.END)
        
        self.log_file.write(f"{timestamp}: {temperatura} °C\n")
        self.log_file.flush()

    def fechar_janela(self):
        self.log_file.close()
        self.root.quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TemperaturaApp(root)
    root.protocol("WM_DELETE_WINDOW", app.fechar_janela)
    root.mainloop()
