import time
import random
import requests
from playwright.sync_api import sync_playwright

# =========================
# CONFIG
# =========================

TELEGRAM_TOKEN = "8507528681:AAEK836H9FfVZ0ZdoGBgCSR--J4gjX7L-uM"
CHAT_ID = "5345823250"

LINKS = {
    "Brasil x Marrocos": "https://fwc26-shop-usd.tickets.fifa.com/secure/selection/event/seat/performance/10229226700891/contact-advantages/10229997072863,10230003371090/table/1/lang/en",
    "Brasil x Haiti": "https://fwc26-shop-usd.tickets.fifa.com/secure/selection/event/seat/performance/10229226700917/contact-advantages/10229997072863,10230003371090/table/1/lang/en"
}

# =========================
# TELEGRAM
# =========================

def enviar_telegram(msg):
    if TELEGRAM_TOKEN == "" or CHAT_ID == "":
        print(f"[TELEGRAM OFF] {msg}")
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    except:
        pass

# =========================
# DETECÇÃO FIFA
# =========================

def verificar_pagina(page, nome):
    html = page.content().lower()

    if any(x in html for x in ["captcha", "queue", "fila", "blocked"]):
        print(f"🔒 {nome} -> bloqueado (fila/captcha)")
        return "bloqueado"

    if any(x in html for x in ["add to cart", "buy", "purchase"]):
        print(f"🚨 {nome} -> DISPONÍVEL")
        enviar_telegram(f"🚨 INGRESSO DISPONÍVEL: {nome}")
        return "disponivel"

    if "option" in html and ">0<" in html:
        print(f"🟡 {nome} -> dropdown ativo")
        enviar_telegram(f"🟡 POSSÍVEL LIBERAÇÃO: {nome}")
        return "quase"

    if any(x in html for x in ["unavailable", "sold out", "not available"]):
        print(f"⚪ {nome} -> fechado")
        return "fechado"

    print(f"⚪ {nome} -> fechado (default)")
    return "fechado"

# =========================
# LOOP PRINCIPAL
# =========================

def main():
    print("🚀 ULTRA SNIPER FIFA ATIVO")

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--no-sandbox", "--disable-setuid-sandbox"]
        )

        # 🧠 CONTEXTO HUMANIZADO
        context = browser.new_context(
            user_agent=random.choice([
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36"
            ]),
            viewport={"width": random.choice([1366, 1440, 1536]), "height": random.choice([768, 900, 864])},
            locale="en-US"
        )

        page = context.new_page()

        while True:
            print("\n🔄 NOVO CICLO ----------------------")

            for nome, link in LINKS.items():
                try:
                    print(f"🌐 Acessando {nome}...")

                    page.goto(link, timeout=60000)

                    # ⏱️ tempo humano variável
                    time.sleep(random.uniform(3, 5))

                    status = verificar_pagina(page, nome)

                    # ⏳ delays inteligentes
                    if status == "bloqueado":
                        print("🧊 cooldown ativado...")
                        time.sleep(random.uniform(12, 18))
                    elif status == "quase":
                        time.sleep(random.uniform(6, 10))
                    else:
                        time.sleep(random.uniform(5, 8))

                except Exception as e:
                    print(f"❌ Erro em {nome}: {e}")
                    time.sleep(6)

            # ⏳ pausa geral (SUPER IMPORTANTE)
            print("⏳ aguardando próximo ciclo...\n")
            time.sleep(random.uniform(12, 20))

# =========================

if __name__ == "__main__":
    main()
