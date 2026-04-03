import requests
import time
import random
from flask import Flask

TOKEN = "8507528681:AAEK836H9FfVZ0ZdoGBgCSR--J4gjX7L-uM"
CHAT_ID = "5345823250"

URLS = [
    ("Brasil x Marrocos", "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/seat?perfId=10229226700891"),
    ("Brasil x Haiti", "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/seat?perfId=10229226700917")
]

# 🔥 sessão fixa por jogo
sessions = {
    nome: requests.Session() for nome, _ in URLS
}

# 🔥 controle de bloqueio
cooldown = {
    nome: 0 for nome, _ in URLS
}

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

def checar(nome, url):
    try:
        session = sessions[nome]

        # visita home
        session.get("https://tickets.fifa.com", headers=get_headers(), timeout=10)

        time.sleep(random.uniform(2, 5))

        r = session.get(url, headers=get_headers(), timeout=10)

        return detectar(r.text)

    except Exception as e:
        enviar(f"⚠️ ERRO\n{nome}\n{str(e)}")
        return None

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot rodando"

def rodar():
    print("🚀 BOT INICIANDO...", flush=True)
    enviar("🚀 ULTRA SNIPER V3 ATIVO")

    enviados = set()

    while True:
        print("🔁 NOVO CICLO ---------------------", flush=True)

        agora = time.time()

        for nome, url in URLS:

            # ⛔ respeita cooldown
            if agora < cooldown[nome]:
                print(f"⏳ {nome} em cooldown", flush=True)
                continue

            status = checar(nome, url)

            print(f"🔎 {nome} → {status}", flush=True)

            if status == "bloqueado":
                # 🔥 pausa maior se bloqueado
                cooldown[nome] = time.time() + random.uniform(30, 60)
                print(f"🛑 {nome} entrou em cooldown", flush=True)
                continue

            elif status == "disponivel":
                if nome not in enviados:
                    enviar(f"🚨 INGRESSOS LIBERADOS!\n\n{nome}\n👉 {url}")
                    enviados.add(nome)

            # delay humano entre jogos
            time.sleep(random.uniform(4, 8))

        # pausa geral
        time.sleep(random.uniform(6, 12))

if __name__ == "__main__":
    import threading
    threading.Thread(target=rodar).start()
    app.run(host="0.0.0.0", port=10000)
