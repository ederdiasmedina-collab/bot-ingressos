import time
import random
import requests
import os
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

INIT_FILE = "started.flag"

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
        print("📩 Telegram:", response.status_code)
    except Exception as e:
        print("Erro Telegram:", e)

# ============================
# DETECÇÃO COMPLETA
# ============================

def verificar_pagina(page, nome):
    html = page.content().lower()

    # BLOQUEIO
    if "captcha" in html or "blocked" in html:
        print(f"🔒 {nome} -> bloqueado")
        return "bloqueado"

    # DISPONÍVEL (principal)
    if "add to cart" in html:
        print(f"🚨 {nome} -> DISPONÍVEL (add to cart)")
        enviar_telegram(f"🚨 INGRESSO DISPONÍVEL: {nome}")
        return "disponivel"

    # BOTÃO CONTINUE ATIVO
    if "continue" in html and "disabled" not in html:
        print(f"🚨 {nome} -> possível compra liberada")
        enviar_telegram(f"🚨 POSSÍVEL COMPRA LIBERADA: {nome}")
        return "disponivel"

    # DROPDOWN / QUANTIDADE
    if "option" in html and (">0<" in html or ">1<" in html or ">2<" in html):
        print(f"🟡 {nome} -> quantidade detectada")
        enviar_telegram(f"🟡 QUANTIDADE DISPONÍVEL: {nome}")
        return "quase"

    # TELA DE ASSENTOS
    if "seat" in html or "table" in html:
        print(f"🟡 {nome} -> tela de seleção carregada")
        return "quase"

    # ESGOTADO
    if "sold out" in html:
        print(f"❌ {nome} -> esgotado")
        return "fechado"

    print(f"🔎 {nome} -> fechado")
    return "fechado"

# ============================
# BOT
# ============================

def rodar():
    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-blink-features=AutomationControlled"
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
# START CONTROLADO
# ============================

if __name__ == "__main__":
    print("🚀 BOT INICIANDO...")

    if not os.path.exists(INIT_FILE):
        enviar_telegram("🤖 BOT INICIADO COM SUCESSO")
        with open(INIT_FILE, "w") as f:
            f.write("ok")

    rodar()
