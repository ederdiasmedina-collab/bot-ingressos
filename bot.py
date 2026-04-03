import time
import random
import requests
from playwright.sync_api import sync_playwright

# ============================
# CONFIG
# ============================

LINKS = {
    "Brasil x Marrocos": "https://fwc26-shop-usd.tickets.fifa.com/secure/selection/event/seat/performance/10229226700891/contact-advantages/10229997072863,10230003371090/table/1/lang/en",
    "Brasil x Haiti": "https://fwc26-shop-usd.tickets.fifa.com/secure/selection/event/seat/performance/10229226700917/contact-advantages/10229997072863,10230003371090/table/1/lang/en"
}

TELEGRAM_TOKEN = "8507528681:AAEK836H9FfVZ0ZdoGBgCSR--J4gjX7L-uM"
CHAT_ID = "5345823250"

# ============================
# TELEGRAM
# ============================

def enviar_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        response = requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": msg
        })

        # DEBUG (importante pra você ver se está funcionando)
        print("📩 Telegram status:", response.status_code)

    except Exception as e:
        print("Erro Telegram:", e)

# ============================
# DETECÇÃO
# ============================

def verificar_pagina(page, nome):
    html = page.content().lower()

    if "captcha" in html or "blocked" in html:
        print(f"🔒 {nome} -> bloqueado")
        return "bloqueado"

    if "add to cart" in html:
        print(f"🚨 {nome} -> DISPONÍVEL")
        enviar_telegram(f"🚨 INGRESSO DISPONÍVEL: {nome}")
        return "disponivel"

    if "option" in html and ">0<" in html:
        print(f"🟡 {nome} -> possível liberação")
        enviar_telegram(f"🟡 POSSÍVEL LIBERAÇÃO: {nome}")
        return "quase"

    print(f"🔎 {nome} -> fechado")
    return "fechado"

# ============================
# BOT
# ============================

def rodar():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            channel="chromium",
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox"
            ]
        )

        context = browser.new_context(
            user_agent=random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                "Mozilla/5.0 (X11; Linux x86_64)"
            ])
        )

        while True:
            print("\n🔄 NOVO CICLO ----------------------")

            for nome, link in LINKS.items():
                page = context.new_page()

                try:
                    page.goto(link, timeout=60000)

                    time.sleep(random.uniform(3, 6))

                    status = verificar_pagina(page, nome)

                    if status == "bloqueado":
                        print(f"⛔ {nome} entrou em cooldown")
                        time.sleep(random.uniform(25, 45))

                except Exception as e:
                    print(f"⚠️ erro em {nome}: {e}")

                finally:
                    page.close()

                time.sleep(random.uniform(5, 10))

            time.sleep(random.uniform(20, 40))


# ============================
# START
# ============================

if __name__ == "__main__":
    print("🚀 BOT INICIADO")
    enviar_telegram("🤖 BOT INICIADO COM SUCESSO")
    rodar()
