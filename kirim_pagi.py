"""Kirim satu lontar tersegel ke Telegram setiap pagi (dijalankan GitHub Actions).

Butuh 3 secret di repo GitHub:
  BOT_TOKEN  - token dari @BotFather
  CHAT_ID    - ID chat Telegram-mu (angka)
  APP_URL    - alamat GitHub Pages, contoh: https://fokushunter07.github.io/suluh/
"""
import json, os, random, urllib.request, html

TOKEN = os.environ["BOT_TOKEN"]
CHAT = os.environ["CHAT_ID"]
URL = os.environ["APP_URL"].rstrip("/") + "/"

data = json.load(open("kartu.json", encoding="utf-8"))
rak = {b["id"]: b for b in data["rak"]}
k = random.choice(data["kartu"])

teks = (
    "🕯 <b>Lontar pagi ini</b>\n\n"
    f"<i>{html.escape(k['h'])}</i>\n\n"
    f"— {html.escape(rak[k['b']]['t'])}"
)
body = {
    "chat_id": CHAT,
    "text": teks,
    "parse_mode": "HTML",
    "reply_markup": {"inline_keyboard": [[{"text": "Buka lontar", "web_app": {"url": f"{URL}?k={k['id']}"}}]]},
}
req = urllib.request.Request(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    data=json.dumps(body).encode(),
    headers={"Content-Type": "application/json"},
)
print(urllib.request.urlopen(req).read().decode()[:200])
