import time
import random
from playwright.sync_api import sync_playwright
import requests

# ==============================
# CONFIG
# ==============================

TELEGRAM_TOKEN = "8507528681:AAEK836H9FfVZ0ZdoGBgCSR--J4gjX7L-uM"
CHAT_ID = "5345823250"

LINKS = {
    "Brasil x Marrocos": "COLE_LINK_AQUI",
    "Brasil x Haiti": "COLE_LINK_AQUI"
}

# ==============================
# TELEGRAM
# ==============================

def enviar_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

# ==============================
# DETECÇÃO
# ==============================

def verificar_pagina(page, nome):
    html = page.content()

    # sinais de bloqueio
    if "captcha" in html.lower():
        print(f"🔒 {nome} → bloqueado")
        return "bloqueado"

    # botão add to cart ativo
    if "Add to cart" in html or "add to cart" in html:
        print(f"🚨 {nome} → DISPONÍVEL")
        enviar_telegram(f"🚨 INGRESSO DISPONÍVEL: {nome}")
        return "disponivel"

    # dropdown (0 com seta)
    if "option" in html and "0" in html:
        print(f"🟡 {nome} → dropdown ativo")
        enviar_telegram(f"🟡 POSSÍVEL LIBERAÇÃO: {nome}")
        return "quase"

    print(f"🔎 {nome} → fechado")
    return "fechado"

# ==============================
# BOT PRINCIPAL
# ==============================

def rodar():
    print("🚀 BOT ELITE (BROWSER REAL) ATIVO")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)

        while True:
            print("\n🔁 NOVO CICLO ----------------")

            for nome, link in LINKS.items():
                context = browser.new_context(
                    user_agent=random.choice([
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
                        "Mozilla/5.0 (X11; Linux x86_64)"
                    ])
                )

                page = context.new_page()

                try:
                    print(f"🌐 Acessando {nome}")
                    page.goto(link, timeout=60000)

                    time.sleep(random.uniform(3, 6))

                    verificar_pagina(page, nome)

                except Exception as e:
                    print(f"⚠️ Erro em {nome}: {e}")

                finally:
                    context.close()

                time.sleep(random.uniform(5, 10))

            # pausa maior pra evitar bloqueio
            time.sleep(random.uniform(20, 40))


# ==============================
# START
# ==============================

if __name__ == "__main__":
    rodar()
