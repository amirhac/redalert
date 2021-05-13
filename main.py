from datetime import datetime
import requests
import yaml


with open(r'config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

SECONDS_THRESHOLD = config['SECONDS_THRESHOLD']
AREAS = config['AREAS']
TELEGRAM_BOT_TOKEN = config['TELEGRAM_BOT_TOKEN']
CHAT_IDS = config['CHAT_IDS']

def is_red_alert():
    alerts = requests.get("https://www.oref.org.il/WarningMessages/History/AlertsHistory.json").json()
    true_alerts = []
    for alert in alerts:
        alert_time = datetime.strptime(alert['alertDate'], '%Y-%m-%d %H:%M:%S')
        area = alert['data']
        seconds_since_alert = (datetime.now() - alert_time).seconds
        if seconds_since_alert < SECONDS_THRESHOLD and area in AREAS:
            true_alerts.append(alert)
            print(alert)

    if true_alerts:
        return true_alerts
    else:
        return None


def send_telegram(msg):
    url = "https://api.telegram.org/bot%s/sendMessage" % TELEGRAM_BOT_TOKEN
    for id in CHAT_IDS:
        requests.post(url, data={"chat_id": id, "text": msg})


alerts = is_red_alert()
if alerts:
    send_telegram("RED ALERT\n" + alerts[0]['alertDate'] + "\n" + alerts[0]['data'])