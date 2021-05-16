import json

import requests
import yaml
import paho.mqtt.client as mqtt

with open(r'config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

SECONDS_THRESHOLD = config['SECONDS_THRESHOLD']
AREAS = config['AREAS']
TELEGRAM_BOT_TOKEN = config['TELEGRAM_BOT_TOKEN']
CHAT_IDS = config['CHAT_IDS']

telegram_enabled = False

mqttc = mqtt.Client("redalert")
mqttc.connect("localhost", 1884)
mqttc.loop_start()


def is_red_alert():
    headers = {
        "Referer": "https://www.oref.org.il/12481-he/Pakar.aspx".encode(),
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8".encode(),
        "X-Requested-With": "XMLHttpRequest",
    }

    alerts = requests.get("http://www.oref.org.il/WarningMessages/Alert/alerts.json", headers=headers).text
    if alerts != "":
        data = json.loads(alerts)
        areas = set(data['data']) & set(AREAS)
        if areas or True:
            msg = "RED ALERT in " + str(data)
            print(msg)
            send_telegram(msg)
            send_mqtt("on")
        else:
            send_mqtt("off")
    else:
        send_mqtt("off")


def send_telegram(msg):
    if telegram_enabled:
        url = "https://api.telegram.org/bot%s/sendMessage" % TELEGRAM_BOT_TOKEN
        for id in CHAT_IDS:
            requests.post(url, data={"chat_id": id, "text": msg})


def send_mqtt(msg):
    mqttc.publish("redalert/alert", msg)
    mqttc.loop_stop()


try:
    while True:
        is_red_alert()
finally:
    mqttc.loop_stop()
