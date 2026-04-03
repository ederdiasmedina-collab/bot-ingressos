import requests
import time
import os

TOKEN = "8507528681:AAFLwuapM0KwJ4mJ9pNQ_kikTA7pQL30k1Q"
CHAT_ID = "5345823250"

URLS = {
    "Brasil x Marrocos": "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/seat?perfId=10229226700891",
    "Brasil x Haiti": "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/seat?perfId=10229226700917"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def enviar_mensagem(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": msg
    })

def verificar():
    liberado = []

    for nome, url in URLS.items():
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)

            # 🔥 CORREÇÃO PRINCIPAL (evita falso alerta)
            if "Buy tickets" in r.text or "Add to cart" in r.text:
                liberado.append(f"{nome}\n👉 {url}")

        except:
            print("Erro ao acessar:", nome)

    return liberado

# 👇 servidor fake pra manter online (OBRIGATÓRIO no plano free)
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot rodando"

def rodar_bot():
    print("🔎 Monitorando ingressos...")
    enviados = set()

    while True:
        print("Rodando loop...")

        resultados = verificar()

        if resultados:
            novos = [r for r in resultados if r not in enviados]

            if novos:
                msg = "🚨 INGRESSOS LIBERADOS!\n\n" + "\n\n".join(novos)
                enviar_mensagem(msg)
                enviados.update(novos)

        time.sleep(30)  # 🔥 velocidade (30s)

# 👇 roda os dois juntos
import threading

if __name__ == "__main__":
    threading.Thread(target=rodar_bot).start()
    app.run(host="0.0.0.0", port=10000)
