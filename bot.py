import requests
import time
import threading
from flask import Flask

# 🔑 CONFIGURE AQUI
TOKEN = "8507528681:AAEK836H9FfVZ0ZdoGBgCSR--J4gjX7L-uM"
CHAT_ID = "5345823250"

# 🎯 prioridade (Brasil primeiro)
URLS = [
    ("Brasil x Marrocos", "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/seat?perfId=10229226700891"),
    ("Brasil x Haiti", "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/seat?perfId=10229226700917"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive"
}

# 🔥 sessão global (cookies + performance)
session = requests.Session()

def enviar(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        session.post(url, json={"chat_id": CHAT_ID, "text": msg}, timeout=5)
    except:
        print("Erro ao enviar mensagem")


# 🧠 DETECÇÃO ULTRA PRECISA
def detectar(html):
    t = html.lower()

    # 🚫 bloqueios
    if any(x in t for x in ["captcha", "queue", "access denied"]):
        return "BLOQUEADO"

    # ❌ indisponível
    if "currently unavailable" in t:
        return False

    # 🔥 ULTRA: dropdown real (0 ▼)
    sinais_dropdown = [
        "<select",
        "option value",
        "quantity",
        "select quantity"
    ]

    if any(s in t for s in sinais_dropdown):
        return "ULTRA"

    # 🟢 secundário
    if "add to cart" in t:
        return "CONFIRMADO"

    # 🟡 pré-sinal
    if "high demand" in t:
        return "QUASE"

    return False


def checar(nome, url):
    try:
        r = session.get(url, headers=HEADERS, timeout=5)
        return nome, url, detectar(r.text)
    except Exception as e:
        enviar(f"⚠️ ERRO\n{nome}\n{str(e)}")
        return nome, url, None


# 🌐 servidor fake (Render)
app = Flask(__name__)

@app.route('/')
def home():
    return "online"


def rodar():
    enviar("🚀 BOT ULTRA SNIPER ATIVO")

    enviados = set()
    delay = 20
    ultimo_heartbeat = time.time()

    while True:
        try:
            threads = []
            resultados = []

            # ⚡ paralelo
            def worker(nome, url):
                res = checar(nome, url)
                resultados.append(res)

            for nome, url in URLS:
                t = threading.Thread(target=worker, args=(nome, url))
                t.start()
                threads.append(t)

            for t in threads:
                t.join()

            for nome, url, status in resultados:

                if not status:
                    continue

                chave = f"{status}-{nome}"
                if chave in enviados:
                    continue

                if status == "ULTRA":
                    enviar(f"🔥🔥🔥 ULTRA SNIPER\n\n{nome}\n👉 {url}")
                    delay = 3  # ⚡ máximo

                elif status == "CONFIRMADO":
                    enviar(f"🚨 INGRESSOS\n\n{nome}\n👉 {url}")
                    delay = 6

                elif status == "QUASE":
                    enviar(f"⚠️ FIQUE ATENTO\n\n{nome}")
                    delay = 10

                elif status == "BLOQUEADO":
                    enviar(f"🛑 BLOQUEADO\n{nome}")
                    delay = 60

                enviados.add(chave)

            # ❤️ heartbeat
            if time.time() - ultimo_heartbeat > 600:
                enviar("🤖 Bot ativo")
                ultimo_heartbeat = time.time()

            time.sleep(delay)

        except Exception as e:
            enviar(f"🔥 ERRO CRÍTICO\n{str(e)}")
            time.sleep(60)


# 🚀 execução
if __name__ == "__main__":
    threading.Thread(target=rodar).start()
    app.run(host="0.0.0.0", port=10000)
