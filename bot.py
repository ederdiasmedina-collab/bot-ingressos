import requests
import time

BOT_TOKEN = "8507528681:AAFLwuapM0KwJ4mJ9pNQ_kikTA7pQL3oklQ"
CHAT_ID = "5345823250"

URL = "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/date?productId=10229225515651"

links = {
    "Brasil x Marrocos": "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/seat?perfId=10229226700891&table=1&productId=10229225515651",
    "Brasil x Haiti": "https://fwc26-shop-usd.tickets.fifa.com/secured/selection/event/seat?perfId=10229226700917&table=1&productId=10229225515651"
}

def enviar(msg):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            data={"chat_id": CHAT_ID, "text": msg},
            timeout=5
        )
    except:
        pass

print("🔎 Monitorando ingressos...")
enviar("✅ BOT INICIADO")

avisado = False

while True:
    print("Rodando loop...")

    try:
        r = requests.get(URL, timeout=5)

        # 👇 Só continua se for JSON válido
        if "application/json" not in r.headers.get("Content-Type", ""):
            print("Resposta inválida (não JSON)")
            time.sleep(5)
            continue

        data = r.json()
        performances = data.get("performances", [])

        if len(performances) > 0:
            if not avisado:
                mensagem = "🚨 INGRESSOS LIBERADOS!\n\n"

                for nome, link in links.items():
                    mensagem += f"{nome}\n👉 {link}\n\n"

                enviar(mensagem)
                avisado = True
        else:
            print("Ainda fechado...")

    except:
        print("Erro ignorado (normal)")

    time.sleep(10)
