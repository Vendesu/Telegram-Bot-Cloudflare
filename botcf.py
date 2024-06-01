import telebot
import requests
import json
import re
from datetime import datetime
import random
import string

# Konfigurasi Bot dan Cloudflare
TELEGRAM_TOKEN = "7127570979:AAHY7ATgQc79AbRSHDtm-Tc5c3x3Wx267YQ"
DEFAULT_DOMAIN = "infinityxssh.com"
CLOUDFLARE_EMAIL = "pendetot@gmail.com"
CLOUDFLARE_TOKEN = "30998e06f35cc33413dc8ec97f94d4297a39a"
CLOUDFLARE_ZONE_ID = "ea20bb7f4ea2be997d483c710c4642c3"

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

Update Chanel : https://t.me/ariasbotupdate
Grup Telegram : https://t.me/ariazbottools
Requests tools bot bisa di grup
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
    subdomain_name = f"ariaz{random_keyword}"

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
            f"✅ Subdomain {full_domain} berhasil dibuat! 🎉\n\nIP: {ip}\nCreated At: {created_at.strftime('%d %B %Y, %H:%M:%S UTC')}",
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


if __name__ == "__main__":
    bot.polling(none_stop=True)
