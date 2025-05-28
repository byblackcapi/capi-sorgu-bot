# 🤖 Capi Sorgu Botu — Mısır Taht'tan Bilgi Akıyor!

Telegram üzerinden TC, GSM, tapu, adres, aile ve daha fazlasını hızlıca sorgulayan, `.txt` çıktılarıyla profesyonel çalışan **açık kaynak bir bot!**

[![Telegram Destek](https://img.shields.io/badge/Telegram-@capiyedek-blue?logo=telegram)](https://t.me/capiyedek)
![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Lisansa Açık](https://img.shields.io/github/license/byblackcapi/capi-sorgu-bot)

📦 Capi Sorgu Botu

Telegram üzerinden gelişmiş kişi/veri sorgulama yapabilen, Python tabanlı bir Telegram botudur. Her sorguyu `.txt` dosyası olarak çıktı verir. Sade arayüzü, kapsamlı API desteği ve hataya dayanıklı yapısıyla öğrenme ve test amaçlı kullanıma uygundur.

🚀 Özellikler

- 19+ adet özelleştirilmiş REST API ile sorgulama
- Tüm sonuçlar `.txt` dosyası halinde kullanıcıya iletilir
- Kullanıcı dostu `/start`, `/help`, `/servisler` komutları
- Her API çağrısı detaylı olarak `bot.log` dosyasına kaydedilir
- Hatalı komutlara karşı rehberlik eden mesajlar
- Gelişmiş hata yönetimi ve loglama
- AIOHTTP ile asenkron HTTP sorguları
- Her API için otomatik handler oluşturma

🛠️ Kullanılan Teknolojiler

- Python 3.10+
- python-telegram-bot v20+ – Telegram bot çatısı
- aiohttp – Asenkron HTTP sorguları
- asyncio – Asenkron yapı
- logging – Kapsamlı loglama
- re – Regex desteğiyle komut ayrıştırma

⚙️ Kurulum

# Sanal ortam oluştur (isteğe bağlı)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Gereken kütüphaneleri yükle
pip install python-telegram-bot aiohttp

Botu çalıştırmak için:

python bot.py

Not: Bot tokenı bot.py içinde os.getenv("TELEGRAM_TOKEN", "buraya token gircen aq") satırı ile tanımlıdır. Dilersen doğrudan değiştirebilir veya çevresel değişkenle çalıştırabilirsin.

📌 Komutlar

Aşağıdaki tüm komutlar, başarıyla çalıştığında `.txt` dosyası olarak çıktı üretir:

/tc <tcno>              -> TC ile temel kimlik bilgisi
/gsm <numara>           -> GSM numarası ile kime ait bilgisi
/gsmdetay <numara>      -> GSM için daha fazla detay
/tcpro <tcno>           -> TC detaylı sorgu
/tcgsm <tcno>           -> TC'den GSM çekme
/tapu <tcno>            -> Tapu (mülkiyet) bilgileri
/sulale <tcno>          -> Soy ağacı/sülale bilgileri
/okulno <tcno>          -> Okul numarası bilgisi
/isyeriyetkili <tcno>   -> İş yeri yetkilisi sorgusu
/isyeri <tcno>          -> İşyeri bilgileri
/hane <tcno>            -> Hanede yaşayan diğer kişiler
/adres <tcno>           -> TC ile adres bilgisi
/anne <tcno>            -> Anne bilgileri
/baba <tcno>            -> Baba bilgileri
/aile <tcno>            -> Aile üyeleri bilgisi
/adsoyad <ad> <soyad>   -> Ad soyad ile sorgu
/adsoyadil <ad> <soyad> <il> -> Ad soyad il ile sorgu
/telegram <username>    -> Telegram kullanıcı adı kontrolü

💡 Örnek Kullanımlar

/tc 12345678910
/gsm 05551234567
/adsoyad roket+ali atar
/adsoyadil roket+ali atar bursa
/telegram capiyedek

İki kelimelik ad/soyadlar için aralara + koymalısın. Örneğin: roket+ali

🧠 Botun Mimari Yapısı

🔁 Otomatik Komut Tanıma
- APIS sözlüğünde tanımlı olan her API için otomatik olarak CommandHandler oluşturulur.
- Böylece yeni API eklemek için sadece sözlüğe URL eklemek yeterlidir.

📦 Dosya Bazlı Çıktı Sistemi
- Her API çağrısı sonrası gelen veriler JSON olarak işlenir.
- Sonuçlar okunabilir .txt formatına çevrilip kullanıcıya gönderilir.
- Telegram karakter sınırları aşılmadan detaylı içerik iletilebilir.

📑 Loglama Sistemi
- Her API çağrısı log dosyasına yazılır (tarih, saat, durum kodu, URL).
- Hatalar ayrıntılı biçimde bot.log dosyasında saklanır.

🧩 Hata Yönetimi
- JSON dönüşmeyen yanıtlar da "raw" olarak kullanıcıya iletilir.
- Eksik parametre, bozuk API veya ağ hatalarında kullanıcı bilgilendirilir.

🧪 Test & Geliştirme

Yeni API eklemek çok kolay:

APIS["yenikomut"] = "https://api.example.com/yeni.php?param={}"

Bu komut artık /yenikomut deger olarak çalışır.

🧷 Destek

Telegram üzerinden destek: @capiyedek

🛑 Yasal Uyarı

Bu bot sadece eğitim ve geliştirme amacıyla hazırlanmıştır. Paylaşılan örnek API bağlantıları gerçek verilerle çalışmaz. Kötüye kullanım, etik dışı kullanım veya yasal ihlaller geliştiricinin sorumluluğunda değildir.

🧾 Lisans

MIT Lisansı altında dağıtılmaktadır. İstediğiniz gibi kopyalayabilir, değiştirebilir ve geliştirebilirsiniz.
