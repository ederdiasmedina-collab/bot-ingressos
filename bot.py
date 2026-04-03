import time
import random
import threading
import requests
from flask import Flask
from playwright.sync_api import sync_playwright

# 🔑 CONFIGURE AQUI
TOKEN = "8507528681:AAEK836H9FfVZ0ZdoGBgCSR--J4gjX7L-uM"
CHAT_ID = "5345823250"

URLS = [
    ("Brasil x Marrocos", "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/seat?perfId=10229226700891"),
    ("Brasil x Haiti", "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/seat?perfId=10229226700917")
]

def enviar(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": msg
        }, timeout=10)
    except:
        print("Erro ao enviar mensagem", flush=True)

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

def rodar_bot():
    print("🚀 BOT ELITE INICIANDO...", flush=True)
    enviar("🚀 BOT ELITE (BROWSER REAL) ATIVO")

    enviados = set()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        while True:
            print("🔁 NOVO CICLO -----------------", flush=True)

            for nome, url in URLS:
                try:
                    print(f"🌐 Acessando {nome}", flush=True)

                    page.goto(url, timeout=60000)
                    time.sleep(random.uniform(3, 6))

                    html = page.content()
                    status = detectar(html)

                    print(f"🔎 {nome} → {status}", flush=True)

                    if status == "bloqueado":
                        enviar(f"🛑 BLOQUEADO (captcha/fila)\n{nome}")
                        time.sleep(random.uniform(20, 40))
                        continue

                    if status == "disponivel":
                        if nome not in enviados:
                            enviar(f"🚨 INGRESSOS LIBERADOS!\n\n{nome}\n👉 {url}")
                            enviados.add(nome)

                    time.sleep(random.uniform(5, 10))

                except Exception as e:
                    enviar(f"⚠️ ERRO\n{nome}\n{str(e)}")

            time.sleep(random.uniform(15, 30))

# 🌐 servidor (Render)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot rodando"

if __name__ == "__main__":
    threading.Thread(target=rodar_bot).start()
    app.run(host="0.0.0.0", port=10000)
