import requests
import time
import threading
from flask import Flask

# 🔑 CONFIGURE AQUI
TOKEN = "8507528681:AAEK836H9FfVZ0ZdoGBgCSR--J4gjX7L-uM"
CHAT_ID = "5345823250"

URLS = {
    "Brasil x Marrocos": "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/seat?perfId=10229226700891",
    "Brasil x Haiti": "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/seat?perfId=10229226700917"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

session = requests.Session()  # ⚡ MUITO MAIS RÁPIDO

def enviar_mensagem(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        session.post(url, json={
            "chat_id": CHAT_ID,
            "text": msg
        }, timeout=5)
    except:
        print("Erro ao enviar mensagem")

def verificar():
    liberado = []

    for nome, url in URLS.items():
        try:
            r = session.get(url, headers=HEADERS, timeout=5)

            texto = r.text.lower()

            # 🔥 DETECÇÃO MAIS FORTE
            if (
                "buy tickets" in texto
                or "add to cart" in texto
                or "ticket selection" in texto
            ):
                liberado.append(f"{nome}\n👉 {url}")

        except:
            print("Erro ao acessar:", nome)

    return liberado

# 🌐 servidor fake (necessário no free)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot rodando"

def rodar_bot():
    enviar_mensagem("✅ BOT SNIPER ATIVO")

    enviados = set()

    while True:
        resultados = verificar()

        if resultados:
            novos = [r for r in resultados if r not in enviados]

            if novos:
                msg = "🚨 INGRESSOS DETECTADOS!\n\n" + "\n\n".join(novos)
                enviar_mensagem(msg)
                enviados.update(novos)

        time.sleep(10)  # ⚡ MAIS RÁPIDO

# 🚀 roda tudo junto
if __name__ == "__main__":
    threading.Thread(target=rodar_bot).start()
    app.run(host="0.0.0.0", port=10000)
