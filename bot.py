import requests
import time
import random
from flask import Flask

# 🔑 CONFIGURE AQUI
TOKEN = "8507528681:AAEK836H9FfVZ0ZdoGBgCSR--J4gjX7L-uM"
CHAT_ID = "5345823250"

URLS = [
    ("Brasil x Marrocos", "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/seat?perfId=10229226700891"),
    ("Brasil x Haiti", "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/seat?perfId=10229226700917")
]

# 🔥 múltiplas sessões
sessions = [requests.Session() for _ in range(4)]

HEADERS_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)",
    "Mozilla/5.0 (Linux; Android 10)"
]

def get_headers():
    return {
        "User-Agent": random.choice(HEADERS_LIST),
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive"
    }

def enviar(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": msg
        }, timeout=10)
    except:
        print("Erro ao enviar mensagem", flush=True)

# 🔎 DETECÇÃO COMPLETA
def detectar(html):
    html = html.lower()

    if "captcha" in html or "queue" in html:
        return "bloqueado"

    if "currently unavailable" in html:
        return "fechado"

    if (
        'value="0"' in html or
        "add to cart" in html or
        "buy tickets" in html or
        "select your seats" in html or
        "last minute sales" in html
    ):
        return "disponivel"

    return "fechado"

# 🌐 ACESSO HUMANIZADO
def checar(nome, url):
    try:
        session = random.choice(sessions)

        session.get("https://tickets.fifa.com", headers=get_headers(), timeout=10)

        time.sleep(random.uniform(1.5, 3))

        r = session.get(url, headers=get_headers(), timeout=10)

        status = detectar(r.text)

        return nome, url, status

    except Exception as e:
        enviar(f"⚠️ ERRO\n{nome}\n{str(e)}")
        return nome, url, None

# 🌐 servidor fake
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot rodando"

# 🚀 BOT PRINCIPAL
def rodar():
    print("🚀 BOT INICIANDO...", flush=True)
    enviar("🚀 ULTRA SNIPER FIFA ATIVO")

    enviados = set()

    while True:
        print("🔁 NOVO CICLO ---------------------", flush=True)

        for nome, url in URLS:

            nome, url, status = checar(nome, url)

            print(f"🔎 {nome} → {status}", flush=True)

            if status == "bloqueado":
                time.sleep(random.uniform(5, 10))
                continue

            elif status == "disponivel":
                if nome not in enviados:
                    enviar(f"🚨 INGRESSOS LIBERADOS!\n\n{nome}\n👉 {url}")
                    enviados.add(nome)

            time.sleep(random.uniform(2.5, 5))

        time.sleep(random.uniform(5, 8))

# 🚀 START
if __name__ == "__main__":
    import threading
    threading.Thread(target=rodar).start()
    app.run(host="0.0.0.0", port=10000)
