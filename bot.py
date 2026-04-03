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

# 📩 envio telegram
def enviar_mensagem(msg):
    try:
        url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
        requests.post(url, json={
            "chat_id": CHAT_ID,
            "text": msg
        }, timeout=10)
    except:
        print("Erro ao enviar mensagem")

# 🧠 DETECÇÃO ULTRA SNIPER
def detectar_disponibilidade(html):
    texto = html.lower()

    # ❌ bloqueio total
    if "currently unavailable" in texto:
        return False

    # 🟡 sinal antecipado
    alerta = "high demand" in texto

    # 🟢 sinais ULTRA (dropdown de quantidade)
    sinais_ultra = [
        "<select",
        "option value",
        "quantity",
        "select quantity"
    ]

    # 🟢 sinais fortes
    sinais_fortes = [
        "add to cart",
        "buy tickets"
    ]

    if any(s in texto for s in sinais_ultra):
        return "ULTRA"

    if any(s in texto for s in sinais_fortes):
        return "CONFIRMADO"

    if alerta:
        return "QUASE"

    return False


# 🌐 servidor fake (necessário no Render free)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot rodando"

# 🤖 LOOP PRINCIPAL
def rodar_bot():
    enviar_mensagem("🚀 TESTE: bot rodando no Render")
    enviar_mensagem("✅ BOT INICIADO (ULTRA SNIPER)")

    enviados = set()
    delay = 30  # padrão

    while True:
        print("🔄 Verificando...")

        resultados = []

        for nome, url in URLS.items():
            try:
                r = requests.get(url, headers=HEADERS, timeout=10)
                status = detectar_disponibilidade(r.text)

                if status:
                    resultados.append((status, nome, url))

            except:
                print("Erro ao acessar:", nome)

        # 🔥 lógica de envio
        for status, nome, url in resultados:

            chave = f"{status}-{nome}"

            if chave in enviados:
                continue

            if status == "ULTRA":
                msg = f"🔥🔥🔥 ULTRA SNIPER!\n\n{nome}\n👉 {url}"
                delay = 5  # acelera MUITO

            elif status == "CONFIRMADO":
                msg = f"🚨 INGRESSOS LIBERADOS!\n\n{nome}\n👉 {url}"
                delay = 10

            elif status == "QUASE":
                msg = f"⚠️ POSSÍVEL ABERTURA!\n\n{nome}"
                delay = 15

            enviar_mensagem(msg)
            enviados.add(chave)

        time.sleep(delay)


# 🚀 EXECUÇÃO
if __name__ == "__main__":
    threading.Thread(target=rodar_bot).start()
    app.run(host="0.0.0.0", port=10000)
