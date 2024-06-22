![C115](img/c115.png)
# Projeto de Logger de Temperatura

Este projeto consiste em uma aplicação de log de temperatura utilizando uma interface gráfica com Tkinter e comunicação MQTT para publicar e subscrever dados de temperatura.

## Dependências
```
- Python 3.x
- paho-mqtt
- tkinter
```

## Passo-a-passo

### 1. Clonar o Repositório

Primeiro, clone o repositório para sua máquina local:
```bash
git clone https://github.com/seu-usuario/seu-repositorio.git
cd seu-repositorio
```

### 2. Instalar Dependências

Instale as dependências do projeto listadas no arquivo `requirements.txt`:
```bash
pip install -r requirements.txt
```

### 3. Estrutura do Projeto

Aqui está uma visão geral da estrutura de pastas do projeto:

```
my_project/
│
├── src/
│   ├── temperatura_app.py
│   ├── mqtt_publisher.py
│   └── mqtt_logger.py
│
├── logs/
│   └── temperatura_log.txt
│
├── .gitignore
├── README.md
└── requirements.txt
```

### 4. Executar a Aplicação de Interface Gráfica

Para iniciar a aplicação de interface gráfica que exibe e registra a temperatura, execute o seguinte comando:
```bash
python src/temperatura_app.py
```
Você verá uma janela como esta:

1. **Última Temperatura**: Exibe a última temperatura recebida.
2. **Log de Temperaturas**: Mostra o histórico das temperaturas registradas.
3. **Iniciar Logger**: Clique para começar a registrar as temperaturas.
4. **Parar Logger**: Clique para parar o registro das temperaturas.

### 5. Publicar Dados de Temperatura MQTT

Para simular a publicação de dados de temperatura via MQTT, execute:
```bash
python src/mqtt_publisher.py
```
Este script publicará uma leitura de temperatura a cada 5 segundos no tópico MQTT configurado.

### 6. Subscrever e Registrar Dados de Temperatura MQTT

Para subscrever ao tópico MQTT e registrar os dados de temperatura em um arquivo de log, execute:
```bash
python src/mqtt_logger.py
```
Os dados recebidos serão registrados no arquivo `logs/temperatura_log.txt`.

### 7. Encerrando a Aplicação

Para encerrar qualquer uma das aplicações, você pode simplesmente fechar a janela do terminal ou usar `Ctrl+C` no terminal.

---
