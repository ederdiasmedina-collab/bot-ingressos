import time
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
# DETECÇÃO MELHORADA FIFA
# =========================

def verificar_pagina(page, nome):
    html = page.content().lower()

    # 🚫 bloqueio / fila / captcha
    if any(x in html for x in ["captcha", "queue", "fila", "blocked"]):
        print(f"🔒 {nome} -> bloqueado (fila/captcha)")
        return "bloqueado"

    # 🚨 botão ativo
    if any(x in html for x in ["add to cart", "buy", "purchase"]):
        print(f"🚨 {nome} -> DISPONÍVEL")
        enviar_telegram(f"🚨 INGRESSO DISPONÍVEL: {nome}")
        return "disponivel"

    # 🟡 dropdown com 0 (sinal clássico FIFA)
    if "option" in html and ">0<" in html:
        print(f"🟡 {nome} -> dropdown ativo (pré-liberação)")
        enviar_telegram(f"🟡 POSSÍVEL LIBERAÇÃO: {nome}")
        return "quase"

    # 🧠 fallback inteligente
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

        context = browser.new_context()
        page = context.new_page()

        while True:
            print("\n🔄 NOVO CICLO ----------------------")

            for nome, link in LINKS.items():
                try:
                    page.goto(link, timeout=60000)

                    # espera leve pra renderizar (importante FIFA)
                    time.sleep(3)

                    status = verificar_pagina(page, nome)

                    if status == "bloqueado":
                        time.sleep(12)
                    elif status == "quase":
                        time.sleep(6)
                    else:
                        time.sleep(4)

                except Exception as e:
                    print(f"❌ Erro em {nome}: {e}")
                    time.sleep(5)

            # pausa entre ciclos
            time.sleep(8)

# =========================

if __name__ == "__main__":
    main()
