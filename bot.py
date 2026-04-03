import requests
import time
import random
import threading
from flask import Flask

# 🔑 CONFIGURE AQUI
TOKEN = "8507528681:AAEK836H9FfVZ0ZdoGBgCSR--J4gjX7L-uM"
CHAT_ID = "5345823250"

URLS = [
    ("Brasil x Marrocos", "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/seat?perfId=10229226700891"),
    ("Brasil x Haiti", "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/seat?perfId=10229226700917"),
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9",
    "Accept-Language": "en-US,en;q=0.9",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1"
}

session = requests.Session()

def enviar(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        session.post(url, json={"chat_id": CHAT_ID, "text": msg}, timeout=10)
    except:
        print("Erro ao enviar mensagem")


# 🧠 DETECÇÃO FINAL
def detectar(html):
    t = html.lower()

    # 🚫 bloqueios
    if "captcha" in t or "queue" in t:
        return "BLOQUEADO"

    if "access denied" in t:
        return "BANIDO"

    # ❌ indisponível
    if "currently unavailable" in t:
        return False

    # 🥇 ULTRA - dropdown real (0 ▼)
    if any(x in t for x in ["<select", "option value", "quantity"]):
        return "ULTRA"

    # 🥈 CONFIRMADO - botão ativo
    if "add to cart" in t and "disabled" not in t:
        return "CONFIRMADO"

    # 🟡 pré-sinal
    if "high demand" in t:
        return "QUASE"

    return False


# 🌐 servidor fake
app = Flask(__name__)

@app.route('/')
def home():
    return "online"


def rodar():
    enviar("🕵️ BOT STEALTH + SNIPER ATIVO")

    # 🔥 gera cookies reais
    try:
        session.get("https://tickets.fifa.com", headers=HEADERS, timeout=10)
        time.sleep(random.uniform(2, 5))
    except:
        pass

    enviados = set()
    ultimo_heartbeat = time.time()
    delay_base = 12

    while True:
        try:
            print("🔄 Verificando...")

            for nome, url in URLS:
                try:
                    # ⏱️ comportamento humano
                    time.sleep(random.uniform(1.5, 4))

                    r = session.get(url, headers=HEADERS, timeout=10)
                    status = detectar(r.text)

                    if not status:
                        continue

                    chave = f"{status}-{nome}"
                    if chave in enviados:
                        continue

                    if status == "ULTRA":
                        enviar(f"🔥🔥🔥 ULTRA SNIPER\n\n{nome}\n👉 {url}")
                        delay_base = 6

                    elif status == "CONFIRMADO":
                        enviar(f"🚨 INGRESSOS DISPONÍVEIS\n\n{nome}\n👉 {url}")
                        delay_base = 8

                    elif status == "QUASE":
                        enviar(f"⚠️ POSSÍVEL ABERTURA\n\n{nome}")
                        delay_base = 10

                    elif status == "BLOQUEADO":
                        enviar(f"🛑 BLOQUEADO (fila/captcha)\n{nome}")
                        delay_base = 25

                    elif status == "BANIDO":
                        enviar(f"⛔ ACESSO NEGADO\n{nome}")
                        delay_base = 60

                    enviados.add(chave)

                except Exception as e:
                    enviar(f"⚠️ ERRO\n{nome}\n{str(e)}")

            # ❤️ heartbeat
            if time.time() - ultimo_heartbeat > 600:
                enviar("🤖 Bot ativo (stealth)")
                ultimo_heartbeat = time.time()

            # ⏱️ delay variável
            delay = random.uniform(delay_base, delay_base + 5)
            time.sleep(delay)

        except Exception as e:
            enviar(f"🔥 ERRO CRÍTICO\n{str(e)}")
            time.sleep(60)


if __name__ == "__main__":
    threading.Thread(target=rodar).start()
    app.run(host="0.0.0.0", port=10000)
