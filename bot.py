import time
import random
import requests
import os

from playwright.sync_api import sync_playwright

# força caminho do browser (CRUCIAL no Render)
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

# ============================
# CONFIG
# ============================

LINKS = {
    "Brasil x Marrocos": "https://fwc26-shop-usd.tickets.fifa.com/secure/selection/event/seat/performance/10229226700891/contact-advantages/10229997072863,10230003371090/table/1/lang/en",
    "Brasil x Haiti": "https://fwc26-shop-usd.tickets.fifa.com/secure/selection/event/seat/performance/10229226700917/contact-advantages/10229997072863,10230003371090/table/1/lang/en"
}

TELEGRAM_TOKEN = "8507528681:AAEK836H9FfVZ0ZdoGBgCSR--J4gjX7L-uM"
CHAT_ID = "5345823250"

ultima_msg_inicio = 0
ultimo_alerta = {}

# ============================
# TELEGRAM
# ============================

def enviar(msg):
    try:
        requests.post(f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage", data={
            "chat_id": CHAT_ID,
            "text": msg
        })
    except:
        pass

# ============================
# DETECÇÃO
# ============================

def verificar(page, nome):
    html = page.content().lower()

    if "captcha" in html or "blocked" in html:
        return "bloqueado"

    if "add to cart" in html:
        return "disponivel"

    if "continue" in html and "disabled" not in html:
        return "disponivel"

    return "fechado"

# ============================
# ANTI-SPAM
# ============================

def alerta(nome, tipo):
    agora = time.time()
    chave = f"{nome}_{tipo}"

    if chave not in ultimo_alerta or agora - ultimo_alerta[chave] > 300:
        enviar(f"🚨 {tipo} → {nome}")
        ultimo_alerta[chave] = agora

# ============================
# BOT
# ============================

def rodar():
    global ultima_msg_inicio

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-blink-features=AutomationControlled"
            ]
        )

        context = browser.new_context()

        if time.time() - ultima_msg_inicio > 600:
            enviar("🤖 BOT ONLINE")
            ultima_msg_inicio = time.time()

        while True:
            print("\n🔄 NOVO CICLO")

            for nome, link in LINKS.items():
                page = context.new_page()

                try:
                    page.goto(link, timeout=60000)
                    time.sleep(random.uniform(4, 8))

                    status = verificar(page, nome)

                    if status == "disponivel":
                        print(f"🚨 {nome}")
                        alerta(nome, "INGRESSO")

                    elif status == "bloqueado":
                        print(f"🔒 {nome}")
                        time.sleep(30)

                    else:
                        print(f"❌ {nome}")

                except Exception as e:
                    print("Erro:", e)

                finally:
                    page.close()

                time.sleep(random.uniform(10, 20))

            time.sleep(random.uniform(40, 80))


if __name__ == "__main__":
    print("🚀 INICIANDO BOT")
    rodar()
