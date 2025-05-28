import logging
import json
import re
import asyncio
import os
import re
from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from aiohttp import ClientSession, ClientTimeout

# ----------------------
# 1. Gelişmiş Log Ayarları
# ----------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
    handlers=[
        logging.FileHandler("bot.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("MısırTahtBot")

# ----------------------
# 2. Bot Token ve API Listesi
# ----------------------
TOKEN = os.getenv("TELEGRAM_TOKEN", "buraya token gircen aq")
APIS = {
  "adsoyad":    "https://api.example.com/adsoyadilice.php?ad={}&soyad={}",
  "adsoyadil":  "https://api.example.com/adsoyadilce.php?ad={}&soyad={}&il={}",
  "telegram":   "https://api.example.com/telegram_sorgu.php?username={}",
  "tcpro":      "https://api.example.com/tcpro.php?tc={}",
  "tcgsm":      "https://api.example.com/tcgsm.php?tc={}",
  "tapu":       "https://api.example.com/tapu.php?tc={}",
  "sulale":     "https://api.example.com/sulale.php?tc={}",
  "okulno":     "https://api.example.com/okulno.php?tc={}",
  "isyeriyetkili": "https://api.example.com/isyeriyetkili.php?tc={}",
  "isyeri":     "https://api.example.com/isyeri.php?tc={}",
  "hane":       "https://api.example.com/hane.php?tc={}",
  "gsmdetay":   "https://api.example.com/gsmdetay.php?gsm={}",
  "gsm":        "https://api.example.com/gsm.php?gsm={}",
  "baba":       "https://api.example.com/baba.php?tc={}",
  "anne":       "https://api.example.com/anne.php?tc={}",
  "aile":       "https://api.example.com/aile.php?tc={}",
  "tc":         "https://api.example.com/tc.php?tc={}",
  "adres":      "https://api.example.com/adres.php?tc={}"
}

# ----------------------
# 3. API Çağrısı
# ----------------------
async def query_api(url: str) -> dict | list:
    timeout = ClientTimeout(total=10)
    async with ClientSession(timeout=timeout) as session:
        resp = await session.get(url)
        logger.info(f"API çağrısı: {url} | Durum: {resp.status}")
        text = await resp.text(encoding='utf-8')
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"raw": text}

# ----------------------
# 4. Dosya İçin Düz Metin Oluşturma
# ----------------------
def build_plain_text(data) -> str:
    if isinstance(data, dict):
        if 'data' in data:
            content = data['data']
            if isinstance(content, dict):
                return '\n'.join(f"{k}: {v}" for k, v in content.items())
            if isinstance(content, list):
                parts = []
                for i, item in enumerate(content, 1):
                    if isinstance(item, dict):
                        header = f"-- Sonuç {i} --"
                        lines = '\n'.join(f"{k}: {v}" for k, v in item.items())
                        parts.append(header + '\n' + lines)
                    else:
                        parts.append(str(item))
                return '\n\n'.join(parts)
        return json.dumps(data, ensure_ascii=False, indent=2)

    elif isinstance(data, list):
        parts = []
        for i, item in enumerate(data, 1):
            if isinstance(item, dict):
                header = f"-- Sonuç {i} --"
                lines = '\n'.join(f"{k}: {v}" for k, v in item.items())
                parts.append(header + '\n' + lines)
            else:
                parts.append(str(item))
        return '\n\n'.join(parts)

    return str(data)

# ----------------------
# 5. API Komut Handler (Her zaman .txt)
# ----------------------
async def api_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.effective_message
    parts = msg.text.split()
    name = parts[0].lstrip('/')
    args = parts[1:]

    if name not in APIS:
        await msg.reply_text("❌ Geçersiz komut! /help ile listeye bak.")
        return
    try:
        api_response = await query_api(APIS[name].format(*args))
    except Exception as e:
        logger.exception("API isteği başarısız")
        await msg.reply_text(f"🚨 Hata: {e}")
        return

    # Dosya için oluştur
    plain = build_plain_text(api_response)
    filename = f"{name}_sonuc.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(plain)

    # Dosyayı InputFile ile doğru MIME tipiyle gönder
    with open(filename, 'rb') as f:
        input_file = InputFile(f, filename=filename)
        await msg.reply_document(document=input_file, caption=f"📄 {name} sonucu", parse_mode="HTML")

    os.remove(filename)

# ----------------------
# 6. /start Komutu
# ----------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "👋 <b>Merhaba!</b>\n"
        "Ben <i>capi Sorgu Botu</i>.\n\n"
        "🔍 <b>Ne Yapabilirim?</b>\n"
        "• TC, GSM, Adres, Tapu, Aile ve daha fazlası.\n"
        "• Sonuçları her zaman .txt dosyası olarak iletir.\n\n"
        "💡 Komutlar: /help\n"
        "📊 Servisler: /servisler\n"
        "🔗 Destek: <a href='https://t.me/capiyedek'>@capiyedek</a>"
    )
    buttons = [[
        InlineKeyboardButton("📚 Yardım", callback_data='help'),
        InlineKeyboardButton("🚀 Servisler", callback_data='servisler')
    ]]
    await update.effective_message.reply_text(text, parse_mode="HTML", reply_markup=InlineKeyboardMarkup(buttons))

# ----------------------
# 7. /help Komutu
# ----------------------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = [f"• /<b>{cmd}</b>" for cmd in sorted(APIS.keys())]
    examples = [
        "/tc 12345678910 — TC kimlik ile sorgulama",
        "/gsm 05551234567 — GSM numarası ile detay",
        "/adsoyad Ahmet Yılmaz — Ad Soyad sorgusu",
        "/adsoyadil Ahmet Yılmaz İstanbul — Ad, soyad ve il ile sorgu",
        "/telegram capiyedek — Telegram kullanıcı adı kontrolü",
        "/adsoyad roket+ali atar — AdSoyad sorgusunda '+' kullanma",
        "/adsoyadil roket+ali atar bursa — AdSoyadİl sorgusunda '+' kullanım"
    ]
    text = (
        "📖 <b>Komut Listesi:</b>\n\n" +
        "\n".join(lines) +
        "\n\nℹ️ Parametreleri doğru kullandığınızdan emin olun.\n\n" +
        "💡 <b>Örnek Kullanımlar:</b>\n" +
        "\n".join([f"   • {ex}" for ex in examples])
    )
    await update.effective_message.reply_text(text, parse_mode="HTML")

# ----------------------
# 8. /servisler Komutu
# ----------------------
async def servisler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    lines = [f"• /<b>{cmd}</b>" for cmd in sorted(APIS.keys())]
    text = (
        f"🚀 <b>Toplam {len(APIS)} Aktif Servis:</b>\n\n" +
        "\n".join(lines)
    )
    await update.effective_message.reply_text(text, parse_mode="HTML")

# ----------------------
# 9. Bilinmeyen Komut
# ----------------------
async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.effective_message.reply_text(
        "❓ <b>Komutu anlayamadım!</b> /help ile deneyin.", parse_mode="HTML"
    )

# ----------------------
# 10. Bot Başlatma
# ----------------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("servisler", servisler))
    for cmd in APIS.keys():
        app.add_handler(CommandHandler(cmd, api_handler))
    app.add_handler(MessageHandler(filters.COMMAND, unknown))
    logger.info("Bot başlatılıyor...")
    app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
