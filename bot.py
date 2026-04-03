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

# 🌐 sessão persistente (MUITO IMPORTANTE)
session = requests.Session()

HEADERS_LIST = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X)"
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
        print("Erro ao enviar mensagem")

# 🔎 DETECÇÃO INTELIGENTE
def detectar(html):
    html_lower = html.lower()

    # 🚫 BLOQUEIO
    if "captcha" in html_lower or "queue" in html_lower:
        return "bloqueado"

    # 🔥 DISPONÍVEL (3 sinais fortes)
    if (
        "add to cart" in html_lower or
        "buy tickets" in html_lower or
        ('value="0"' in html_lower and "dropdown" in html_lower)
    ):
        return "disponivel"

    return "fechado"

# 🌐 ACESSO HUMANIZADO
def checar(nome, url):
    try:
        # visita home primeiro (simula usuário real)
        session.get("https://tickets.fifa.com", headers=get_headers(), timeout=10)

        time.sleep(random.uniform(2, 4))

        # acessa página do jogo
        r = session.get(url, headers=get_headers(), timeout=10)

        status = detectar(r.text)

        return nome, url, status

    except Exception as e:
        enviar(f"⚠️ ERRO\n{nome}\n{str(e)}")
        return nome, url, None

# 🌐 servidor fake (Render precisa disso)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot rodando"

# 🚀 BOT PRINCIPAL
def rodar():
    enviar("🕵️ BOT STEALTH HUMANO ATIVO")

    enviados = set()

    while True:
        for nome, url in URLS:

            nome, url, status = checar(nome, url)

            if status == "bloqueado":
                enviar(f"🛑 BLOQUEADO (fila/captcha)\n{nome}")

            elif status == "disponivel":
                if nome not in enviados:
                    enviar(f"🚨 INGRESSOS DISPONÍVEIS!\n\n{nome}\n👉 {url}")
                    enviados.add(nome)

            else:
                print(f"{nome}: fechado")

            # ⏱ delay humano entre jogos
            time.sleep(random.uniform(4, 8))

        # ⏱ pausa entre ciclos
        time.sleep(random.uniform(8, 15))

# 🚀 INICIAR
if __name__ == "__main__":
    import threading
    threading.Thread(target=rodar).start()
    app.run(host="0.0.0.0", port=10000)
