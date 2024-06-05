import telebot
import requests
import json
import re
from datetime import datetime
import random
import string
import logging
import schedule
import time
import os
import dotenv


# Check if.env file exists
if not os.path.exists('.env'):
    print("\033[92mSelamat Datang di Pengaturan Bot!\033[0m")  # Green text
    print("\033[93mSilakan isi informasi yang diperlukan:\033[0m")  # Yellow text
    print("\033[94mBot oleh t.me/@bukanaol\033[0m")  # Blue text

    # Mintalah pengguna untuk memasukkan variabel
    TELEGRAM_TOKEN = input("\033[91mMasukkan Token Telegram Anda: \033[0m")
    DEFAULT_DOMAIN = input("\033[91mMasukkan domain default Anda: \033[0m")
    CLOUDFLARE_EMAIL = input("\033[91mMasukkan email Cloudflare Anda: \033[0m")
    CLOUDFLARE_TOKEN = input("\033[91mMasukkan token Cloudflare Anda: \033[0m")
    CLOUDFLARE_ZONE_ID = input("\033[91mMasukkan ID zona Cloudflare Anda: \033[0m")
    CHANNEL_ID = input("\033[91mMasukkan ID channel Telegram Anda: \033[0m")

    # Save variables to.env file
    with open('.env', 'w') as f:
        f.write(f"TELEGRAM_TOKEN={TELEGRAM_TOKEN}\n")
        f.write(f"DEFAULT_DOMAIN={DEFAULT_DOMAIN}\n")
        f.write(f"CLOUDFLARE_EMAIL={CLOUDFLARE_EMAIL}\n")
        f.write(f"CLOUDFLARE_TOKEN={CLOUDFLARE_TOKEN}\n")
        f.write(f"CLOUDFLARE_ZONE_ID={CLOUDFLARE_ZONE_ID}\n")
        f.write(f"CHANNEL_ID={CHANNEL_ID}\n")

    print("Variables saved to.env file!")
else:
    # Load variables from.env file
    dotenv.load_dotenv()
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    DEFAULT_DOMAIN = os.getenv('DEFAULT_DOMAIN')
    CLOUDFLARE_EMAIL = os.getenv('CLOUDFLARE_EMAIL')
    CLOUDFLARE_TOKEN = os.getenv('CLOUDFLARE_TOKEN')
    CLOUDFLARE_ZONE_ID = os.getenv('CLOUDFLARE_ZONE_ID')
    CHANNEL_ID = os.getenv('CHANNEL_ID')

# Rest of the code remains the same
bot = telebot.TeleBot(TELEGRAM_TOKEN)
#...

# Rest of the code remains the same
bot = telebot.TeleBot(TELEGRAM_TOKEN)


# Fungsi Validasi
def validate_ip(ip):
    """Validasi IP address."""
    return re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", ip)


def validate_subdomain_name(subdomain_name):
    """Validasi nama subdomain."""
    return re.match(r"^[a-zA-Z0-9-]+$", subdomain_name)


# Handler untuk perintah /start, /help, dan /about
@bot.message_handler(commands=["start", "help", "about"])
def send_welcome(message):
    """Menampilkan pesan selamat datang dan informasi tentang bot."""
    welcome_message = f"""
👋 Selamat datang di Bot Pembuat Subdomain! 🤖

Halo, {message.from_user.first_name}! Saya dapat membantu Anda membuat subdomain di Cloudflare dengan mudah.

Berikut adalah perintah yang tersedia:

- /add: Membuat subdomain baru.

Update Chanel : @codeplanetch
Grup Telegram : @codeplanethelper

Custom domain mu sendiri chat owner @bukanaol
"""
    bot.reply_to(message, welcome_message)


# Handler untuk perintah /add
@bot.message_handler(commands=["add"])
def handle_buat_subdomain(message):
    """Meminta IP address dari pengguna."""
    bot.send_message(message.chat.id, "Masukkan IP address:")
    bot.register_next_step_handler(message, get_ip)


def get_ip(message):
    """Memvalidasi IP address dan menghasilkan subdomain otomatis."""
    ip = message.text.strip()
    if not validate_ip(ip):
        bot.send_message(message.chat.id, "❌ IP address tidak valid.")
        return

    # Menghasilkan nama subdomain otomatis
    random_keyword = "".join(
        random.choices(string.ascii_lowercase + string.digits, k=5)
    )
    subdomain_name = f"codeplanet{random_keyword}"

    buat_subdomain(message, ip, subdomain_name)  # Panggil buat_subdomain


def buat_subdomain(message, ip, subdomain_name):
    """Membuat subdomain di Cloudflare."""
    full_domain = f"{subdomain_name}.{DEFAULT_DOMAIN}"

    if not validate_subdomain_name(subdomain_name):
        bot.send_message(
            message.chat.id,
            "❌ Nama subdomain tidak valid. Gunakan hanya huruf, angka, dan tanda hubung.",
        )
        return

    headers = {
        "X-Auth-Email": CLOUDFLARE_EMAIL,
        "X-Auth-Key": CLOUDFLARE_TOKEN,
        "Content-Type": "application/json",
    }
    data = {
        "type": "A",
        "name": subdomain_name,
        "content": ip,
        "ttl": 1,
        "proxied": False,
    }

    try:
        response = requests.post(
            f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/dns_records",
            headers=headers,
            data=json.dumps(data),
        )
        response.raise_for_status()

        result = response.json()
        created_at = datetime.now()

        bot.send_message(
            message.chat.id,
           f"✅ Subdomain {full_domain} berhasil dibuat! 🎉\n\nIP: {ip}\nCreated At: {created_at.strftime('%d %B %Y, %H:%M:%S UTC')}\n\nCek Log Di @codeplanetdomainlog",
        ) 
        # Notify the channel
        channel_id = os.getenv('CHANNEL_ID')
        bot.send_message(
            channel_id,
          f"✅ Subdomain XXXXXX berhasil dibuat! 🎉\n\nIP: XXXXXX\nCreated At: {created_at.strftime('%d %B %Y, %H:%M:%S UTC')}\nCreatedBy: @{message.from_user.username}",
        ) 
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            error_data = e.response.json()
            error_messages = [err["message"] for err in error_data.get("errors", [])]
            bot.send_message(
                message.chat.id, f"❌ Terjadi kesalahan: {', '.join(error_messages)}"
            )
        else:
            bot.send_message(
                message.chat.id, f"❌ Terjadi kesalahan saat membuat subdomain: {e}"
            )
    except (requests.exceptions.RequestException, KeyError, json.JSONDecodeError) as e:
        bot.send_message(message.chat.id, f"❌ Terjadi kesalahan yang tidak terduga: {e}")

# Handler untuk pesan yang bukan perintah
@bot.message_handler(func=lambda message: message.text.startswith('/'))
def handle_message(message):
    """Menangani pesan yang bukan perintah."""
    bot.send_message(
        message.chat.id,
        "❌ Perintah tidak valid. Gunakan /help untuk melihat daftar perintah.",
    )

# Konfigurasi logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s",
)

def send_message_every_4_hours():
    # Send a message to a specific chat ID
    chat_id = "@taskforce_store"
    message = "♟️ Bot Aktif! 💻 Mau bikin Subdomain gratis? /add, notif aktif setiap 4jam sekali"
    bot.send_message(chat_id, message)

# Schedule the function to run every 4 hours
schedule.every(4).hours.do(send_message_every_4_hours)

logger = logging.getLogger()

if __name__ == "__main__":
    from termcolor import colored

    logger.info(colored("Bot Cloudflare Run Code By @bukanaol", 'green'))
    bot.polling(none_stop=True)