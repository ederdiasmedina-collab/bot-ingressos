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
# DETECÇÃO MELHORADA
# ============================

def verificar(page, nome):
    html = page.content().lower()

    if "captcha" in html or "blocked" in html:
        print(f"🔒 {nome} BLOQUEADO")
        return "bloqueado"

    if "add to cart" in html:
        return "disponivel"

    if "continue" in html and "disabled" not in html:
        return "disponivel"

    if "option" in html:
        return "quase"

    return "fechado"

# ============================
# ANTI-SPAM TELEGRAM
# ============================

def alerta(nome, tipo):
    agora = time.time()

    chave = f"{nome}_{tipo}"

    if chave not in ultimo_alerta or agora - ultimo_alerta[chave] > 300:
        enviar(f"🚨 {tipo.upper()} → {nome}")
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

        # mensagem única
        if time.time() - ultima_msg_inicio > 600:
            enviar("🤖 BOT ONLINE")
            ultima_msg_inicio = time.time()

        while True:
            print("\n🔄 NOVO CICLO ----------------")

            for nome, link in LINKS.items():
                page = context.new_page()

                try:
                    page.goto(link, timeout=60000)

                    # simula humano
                    time.sleep(random.uniform(4, 8))
                    page.mouse.move(random.randint(100, 500), random.randint(100, 500))

                    status = verificar(page, nome)

                    if status == "disponivel":
                        print(f"🚨 {nome} DISPONÍVEL")
                        alerta(nome, "INGRESSO DISPONÍVEL")

                    elif status == "quase":
                        print(f"🟡 {nome} QUASE")
                        alerta(nome, "QUASE")

                    elif status == "bloqueado":
                        print(f"⛔ {nome} COOLDOWN")
                        time.sleep(random.uniform(30, 60))

                    else:
                        print(f"❌ {nome} fechado")

                except Exception as e:
                    print("Erro:", e)

                finally:
                    page.close()

                time.sleep(random.uniform(10, 20))  # 🔥 MAIS LENTO = menos bloqueio

            time.sleep(random.uniform(40, 80))  # 🔥 CICLO MAIS HUMANO

# ============================
# START
# ============================

if __name__ == "__main__":
    print("🚀 INICIANDO BOT...")
    rodar()
