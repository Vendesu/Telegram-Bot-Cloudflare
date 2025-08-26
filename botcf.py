import telebot
import requests
import json
import re
from datetime import datetime, timedelta
import random
import string
import logging
import schedule
import time
import os
import dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import cloudflare
from cryptography.fernet import Fernet

# Check if .env file exists
if not os.path.exists('.env'):
    print("\033[92mSelamat Datang di Pengaturan Bot!\033[0m")
    print("\033[93mSilakan isi informasi yang diperlukan:\033[0m")
    print("\033[94mBot oleh t.me/@bukanaol\033[0m")

    # Mintalah pengguna untuk memasukkan variabel
    TELEGRAM_TOKEN = input("\033[91mMasukkan Token Telegram Anda: \033[0m")
    DEFAULT_DOMAIN = input("\033[91mMasukkan domain default Anda: \033[0m")
    CLOUDFLARE_API_TOKEN = input("\033[91mMasukkan API Token Cloudflare Anda: \033[0m")
    CLOUDFLARE_ZONE_ID = input("\033[91mMasukkan ID zona Cloudflare Anda: \033[0m")
    CHANNEL_ID = input("\033[91mMasukkan ID channel Telegram Anda: \033[0m")
    DONATION_CHANNEL_ID = input("\033[91mMasukkan ID channel donasi domain: \033[0m")
    
    # Generate encryption key for sensitive data
    ENCRYPTION_KEY = Fernet.generate_key().decode()

    # Save variables to .env file
    with open('.env', 'w') as f:
        f.write(f"TELEGRAM_TOKEN={TELEGRAM_TOKEN}\n")
        f.write(f"DEFAULT_DOMAIN={DEFAULT_DOMAIN}\n")
        f.write(f"CLOUDFLARE_API_TOKEN={CLOUDFLARE_API_TOKEN}\n")
        f.write(f"CLOUDFLARE_ZONE_ID={CLOUDFLARE_ZONE_ID}\n")
        f.write(f"CHANNEL_ID={CHANNEL_ID}\n")
        f.write(f"DONATION_CHANNEL_ID={DONATION_CHANNEL_ID}\n")
        f.write(f"ENCRYPTION_KEY={ENCRYPTION_KEY}\n")

    print("Variables saved to .env file!")
else:
    # Load variables from .env file
    dotenv.load_dotenv()
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    DEFAULT_DOMAIN = os.getenv('DEFAULT_DOMAIN')
    CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
    CLOUDFLARE_ZONE_ID = os.getenv('CLOUDFLARE_ZONE_ID')
    CHANNEL_ID = os.getenv('CHANNEL_ID')
    DONATION_CHANNEL_ID = os.getenv('DONATION_CHANNEL_ID')
    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

# Initialize bot and Cloudflare client
bot = telebot.TeleBot(TELEGRAM_TOKEN)
cf = cloudflare.CloudFlare(token=CLOUDFLARE_API_TOKEN)

# User states for conversation flow
user_states = {}

# Domain donation database (in production, use a proper database)
domain_donations = {}

# Validation functions
def validate_ip(ip):
    """Validate IP address."""
    return re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$", ip)

def validate_subdomain_name(subdomain_name):
    """Validate subdomain name."""
    return re.match(r"^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]$", subdomain_name) and len(subdomain_name) <= 63

def validate_domain(domain):
    """Validate domain name."""
    return re.match(r"^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$", domain)

def generate_subdomain_name():
    """Generate a random subdomain name."""
    adjectives = ["fast", "secure", "reliable", "swift", "powerful", "efficient", "smart", "dynamic"]
    nouns = ["server", "node", "host", "instance", "service", "app", "api", "gateway"]
    
    adj = random.choice(adjectives)
    noun = random.choice(nouns)
    suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=3))
    
    return f"{adj}-{noun}-{suffix}"

def create_main_keyboard():
    """Create the main keyboard."""
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    keyboard.row(KeyboardButton("🚀 Buat Subdomain"), KeyboardButton("💾 Subdomain Saya"))
    keyboard.row(KeyboardButton("🎁 Donasi Domain"), KeyboardButton("📊 Status Bot"))
    keyboard.row(KeyboardButton("ℹ️ Bantuan"), KeyboardButton("👨‍💻 Owner"))
    return keyboard

def create_donation_keyboard():
    """Create donation keyboard."""
    keyboard = InlineKeyboardMarkup()
    keyboard.row(
        InlineKeyboardButton("🌐 Donasi Domain", callback_data="donate_domain")
    )
    keyboard.row(
        InlineKeyboardButton("📋 Lihat Donasi", callback_data="view_donations"),
        InlineKeyboardButton("🔙 Kembali", callback_data="back_to_main")
    )
    return keyboard

# Command handlers
@bot.message_handler(commands=["start", "help", "about"])
def send_welcome(message):
    """Display welcome message and bot information."""
    welcome_message = f"""
🎉 **Selamat Datang di Bot Cloudflare Pro!** 🚀

Halo **{message.from_user.first_name}**! 👋

Saya adalah bot canggih yang dapat membantu Anda:
• 🚀 Membuat subdomain di Cloudflare dengan mudah
• 💾 Mengelola subdomain yang sudah ada
• 🎁 Sistem donasi domain untuk komunitas
• 📊 Monitoring status bot real-time

**Fitur Terbaru:**
✅ Cloudflare API v4 terbaru
✅ Sistem donasi domain
✅ Interface yang lebih modern
✅ Keamanan yang ditingkatkan

**Update Channel:** @codeplanetch
**Grup Telegram:** @codeplanethelper
**Custom Domain:** Chat owner @bukanaol

Gunakan keyboard di bawah untuk memulai! ⬇️
"""
    bot.send_message(
        message.chat.id, 
        welcome_message, 
        parse_mode='Markdown',
        reply_markup=create_main_keyboard()
    )

@bot.message_handler(func=lambda message: message.text == "🚀 Buat Subdomain")
def handle_create_subdomain(message):
    """Handle subdomain creation request."""
    bot.send_message(
        message.chat.id,
        "🌐 **Membuat Subdomain Baru**\n\nSilakan masukkan IP address yang ingin Anda gunakan:",
        parse_mode='Markdown'
    )
    user_states[message.chat.id] = "waiting_for_ip"

@bot.message_handler(func=lambda message: message.text == "💾 Subdomain Saya")
def handle_my_subdomains(message):
    """Show user's subdomains."""
    try:
        # Get DNS records from Cloudflare
        dns_records = cf.zones.dns_records.get(CLOUDFLARE_ZONE_ID)
        
        if not dns_records:
            bot.send_message(message.chat.id, "❌ Tidak ada subdomain yang ditemukan.")
            return
        
        # Filter A records (subdomains)
        a_records = [record for record in dns_records if record['type'] == 'A']
        
        if not a_records:
            bot.send_message(message.chat.id, "❌ Tidak ada subdomain A record yang ditemukan.")
            return
        
        # Create subdomain list
        subdomain_list = "📋 **Daftar Subdomain Anda:**\n\n"
        for record in a_records[:10]:  # Show first 10
            created_date = datetime.fromisoformat(record['created_on'].replace('Z', '+00:00'))
            subdomain_list += f"• **{record['name']}**\n"
            subdomain_list += f"  └ IP: `{record['content']}`\n"
            subdomain_list += f"  └ Dibuat: {created_date.strftime('%d/%m/%Y %H:%M')}\n\n"
        
        if len(a_records) > 10:
            subdomain_list += f"... dan {len(a_records) - 10} subdomain lainnya"
        
        bot.send_message(
            message.chat.id,
            subdomain_list,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ Terjadi kesalahan saat mengambil data subdomain: {str(e)}"
        )

@bot.message_handler(func=lambda message: message.text == "🎁 Donasi Domain")
def handle_donation_menu(message):
    """Show donation menu."""
    donation_text = """
🎁 **Sistem Donasi Domain**

Terima kasih atas ketertarikan Anda untuk berdonasi! 🙏

**Cara berdonasi domain:**
• 🌐 Hubungkan domain Anda ke nameserver Cloudflare kami
• 🔗 Domain akan aktif dan bisa digunakan untuk subdomain
• 🚀 Anda tetap memiliki kontrol penuh atas domain

**Keuntungan berdonasi:**
✅ Akses fitur premium
✅ Prioritas support
✅ Nama Anda di hall of fame
✅ Kontribusi untuk komunitas
✅ Domain tetap milik Anda

Silakan pilih opsi di bawah: ⬇️
"""
    bot.send_message(
        message.chat.id,
        donation_text,
        parse_mode='Markdown',
        reply_markup=create_donation_keyboard()
    )

@bot.message_handler(func=lambda message: message.text == "📊 Status Bot")
def handle_bot_status(message):
    """Show bot status."""
    try:
        # Check Cloudflare API status
        cf_status = "🟢 Online"
        try:
            cf.zones.get()
        except:
            cf_status = "🔴 Offline"
        
        # Bot uptime (simplified)
        uptime = "🟢 Aktif"
        
        status_text = f"""
📊 **Status Bot & Layanan**

🤖 **Bot Status:** {uptime}
☁️ **Cloudflare API:** {cf_status}
🌐 **Domain:** {DEFAULT_DOMAIN}
👥 **Total Users:** {len(user_states)}
⏰ **Last Update:** {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}

**Sistem:** Linux
**Python:** 3.8+
**API Version:** Cloudflare v4
"""
        bot.send_message(
            message.chat.id,
            status_text,
            parse_mode='Markdown'
        )
        
    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"❌ Terjadi kesalahan saat mengecek status: {str(e)}"
        )

@bot.message_handler(func=lambda message: message.text == "ℹ️ Bantuan")
def handle_help(message):
    """Show help information."""
    help_text = """
ℹ️ **Bantuan & Panduan**

**Perintah Dasar:**
• `/start` - Memulai bot
• `/help` - Menampilkan bantuan ini
• `/add` - Membuat subdomain (alternatif)

**Cara Membuat Subdomain:**
1. Klik "🚀 Buat Subdomain"
2. Masukkan IP address yang valid
3. Bot akan membuat subdomain otomatis
4. Subdomain siap digunakan!

**Format IP yang Diterima:**
✅ IPv4: 192.168.1.1
✅ IPv4: 8.8.8.8
❌ IPv6: 2001:db8::1
❌ Domain: example.com

**Support:**
• Owner: @bukanaol
• Channel: @codeplanetch
• Group: @codeplanethelper

**Fitur Donasi:**
Gunakan menu "🎁 Donasi Domain" untuk menghubungkan domain ke nameserver Cloudflare kami!
"""
    bot.send_message(
        message.chat.id,
        help_text,
        parse_mode='Markdown'
    )

@bot.message_handler(func=lambda message: message.text == "👨‍💻 Owner")
def handle_owner_info(message):
    """Show owner information."""
    owner_text = """
👨‍💻 **Informasi Owner**

**Nama:** Bukanaol
**Telegram:** @bukanaol
**Channel:** @codeplanetch
**Group:** @codeplanethelper

**Layanan yang Ditawarkan:**
• 🌐 Custom Domain Setup
• 🚀 VPS Management
• 💻 Web Development
• 🔧 Technical Support

**Kontak untuk:**
• Custom domain setup
• Bot customization
• Technical consultation
• Business partnership

**Jam Kerja:** 24/7 (Response time: 1-24 jam)
"""
    bot.send_message(
        message.chat.id,
        owner_text,
        parse_mode='Markdown'
    )

# Handle IP input for subdomain creation
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_for_ip")
def get_ip_for_subdomain(message):
    """Get IP address and create subdomain."""
    ip = message.text.strip()
    
    if not validate_ip(ip):
        bot.send_message(
            message.chat.id,
            "❌ **IP address tidak valid!**\n\nFormat yang benar:\n• 192.168.1.1\n• 8.8.8.8\n\nSilakan coba lagi:"
        )
        return
    
    # Generate subdomain name
    subdomain_name = generate_subdomain_name()
    
    # Create subdomain
    try:
        # Create DNS record using Cloudflare API
        dns_record = {
            'type': 'A',
            'name': subdomain_name,
            'content': ip,
            'ttl': 1,
            'proxied': False
        }
        
        result = cf.zones.dns_records.post(CLOUDFLARE_ZONE_ID, data=dns_record)
        
        if result:
            created_at = datetime.now()
            full_domain = f"{subdomain_name}.{DEFAULT_DOMAIN}"
            
            success_message = f"""
✅ **Subdomain Berhasil Dibuat!** 🎉

**Detail Subdomain:**
🌐 **Domain:** `{full_domain}`
🔗 **IP Address:** `{ip}`
⏰ **Dibuat:** {created_at.strftime('%d %B %Y, %H:%M:%S UTC')}
👤 **Oleh:** @{message.from_user.username or 'Unknown'}

**Status:** Aktif dan siap digunakan!
**Log:** @codeplanetdomainlog

🎯 **Tips:** Subdomain akan aktif dalam 1-5 menit
"""
            
            bot.send_message(
                message.chat.id,
                success_message,
                parse_mode='Markdown'
            )
            
            # Notify channel
            try:
                bot.send_message(
                    CHANNEL_ID,
                    f"✅ **Subdomain Baru Dibuat!**\n\n🌐 Domain: `{full_domain}`\n🔗 IP: `{ip}`\n👤 Oleh: @{message.from_user.username or 'Unknown'}\n⏰ Waktu: {created_at.strftime('%d/%m/%Y %H:%M:%S')}",
                    parse_mode='Markdown'
                )
            except:
                pass  # Ignore channel notification errors
                
        else:
            bot.send_message(
                message.chat.id,
                "❌ Gagal membuat subdomain. Silakan coba lagi nanti."
            )
            
    except Exception as e:
        error_message = f"""
❌ **Terjadi Kesalahan!**

**Error:** {str(e)}

**Solusi yang bisa dicoba:**
1. Pastikan IP address valid
2. Cek koneksi internet
3. Hubungi owner jika masalah berlanjut

**Support:** @bukanaol
"""
        bot.send_message(
            message.chat.id,
            error_message,
            parse_mode='Markdown'
        )
    
    finally:
        # Clear user state
        if message.chat.id in user_states:
            del user_states[message.chat.id]

# Callback query handler for donation buttons
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    """Handle callback queries from inline keyboards."""
    if call.data == "donate_domain":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "🌐 **Donasi Domain**\n\nSilakan masukkan domain yang ingin dihubungkan ke nameserver Cloudflare kami:\n\nFormat: example.com atau sub.example.com\n\nBot akan memberikan instruksi nameserver yang perlu diatur.",
            parse_mode='Markdown'
        )
        user_states[call.message.chat.id] = "waiting_for_domain_donation"
        

    elif call.data == "view_donations":
        bot.answer_callback_query(call.id)
        if domain_donations:
            donations_text = "🎁 **Daftar Donasi Domain:**\n\n"
            for domain, info in domain_donations.items():
                donations_text += f"🌐 **{domain}**\n"
                donations_text += f"   └ Oleh: @{info['donor']}\n"
                donations_text += f"   └ Status: {info['status']}\n"
                donations_text += f"   └ Tanggal: {info['date']}\n\n"
        else:
            donations_text = "📭 Belum ada donasi domain yang diterima.\n\nJadilah yang pertama untuk berdonasi! 🎉"
        
        bot.send_message(
            call.message.chat.id,
            donations_text,
            parse_mode='Markdown'
        )
        
    elif call.data == "back_to_main":
        bot.answer_callback_query(call.id)
        bot.send_message(
            call.message.chat.id,
            "🏠 **Kembali ke Menu Utama**\n\nSilakan pilih opsi yang tersedia:",
            reply_markup=create_main_keyboard()
        )

# Handle domain donation input
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == "waiting_for_domain_donation")
def handle_domain_donation(message):
    """Process domain donation."""
    domain = message.text.strip()
    
    if not validate_domain(domain):
        bot.send_message(
            message.chat.id,
            "❌ **Domain tidak valid!**\n\nFormat yang benar:\n• example.com\n• sub.example.com\n\nSilakan coba lagi:"
        )
        return
    
    # Store donation (in production, use database)
    domain_donations[domain] = {
        'donor': message.from_user.username or 'Unknown',
        'status': 'Pending',
        'date': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
        'user_id': message.from_user.id
    }
    
    success_message = f"""
🎁 **Terima Kasih atas Donasi Domain!** 🙏

**Domain:** `{domain}`
**Status:** Pending Nameserver Setup
**Tanggal:** {datetime.now().strftime('%d %B %Y, %H:%M:%S')}

**Langkah selanjutnya:**
1. 🔧 Atur nameserver domain Anda ke Cloudflare
2. 📧 Kirim bukti screenshot ke owner
3. ✅ Owner akan verifikasi dan setup
4. 🚀 Domain siap digunakan untuk subdomain!

**Nameserver yang perlu diatur:**
• ns1.cloudflare.com
• ns2.cloudflare.com

**Owner akan menghubungi Anda segera untuk proses selanjutnya.**

**Support:** @bukanaol
"""
    
    bot.send_message(
        message.chat.id,
        success_message,
        parse_mode='Markdown',
        reply_markup=create_main_keyboard()
    )
    
    # Notify donation channel
    try:
        bot.send_message(
            DONATION_CHANNEL_ID,
            f"🎁 **Donasi Domain Baru!**\n\n🌐 Domain: `{domain}`\n👤 Donor: @{message.from_user.username or 'Unknown'}\n🆔 User ID: {message.from_user.id}\n⏰ Tanggal: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\nStatus: Menunggu setup nameserver Cloudflare",
            parse_mode='Markdown'
        )
    except:
        pass
    
    # Clear user state
    if message.chat.id in user_states:
        del user_states[message.chat.id]

# Legacy command handler for /add
@bot.message_handler(commands=["add"])
def handle_legacy_add(message):
    """Handle legacy /add command."""
    bot.send_message(
        message.chat.id,
        "🚀 **Membuat Subdomain**\n\nSilakan masukkan IP address yang ingin Anda gunakan:",
        parse_mode='Markdown'
    )
    user_states[message.chat.id] = "waiting_for_ip"

# Handle unknown commands
@bot.message_handler(func=lambda message: message.text.startswith('/'))
def handle_unknown_command(message):
    """Handle unknown commands."""
    bot.send_message(
        message.chat.id,
        "❌ **Perintah tidak dikenal!**\n\nGunakan keyboard di bawah atau ketik /help untuk bantuan.",
        reply_markup=create_main_keyboard()
    )

# Scheduled tasks
def send_status_update():
    """Send status update every 4 hours."""
    try:
        status_message = """
♟️ **Bot Status Update** 💻

🤖 Bot Cloudflare Pro aktif dan berjalan dengan baik!
🌐 Total subdomain yang dibuat: Berfungsi normal
☁️ Cloudflare API: Responsif
👥 Sistem donasi domain: Tersedia

**Mau bikin subdomain gratis?** 
Klik "🚀 Buat Subdomain" atau ketik /add

**Ingin berdonasi domain?**
Klik "🎁 Donasi Domain" untuk menghubungkan domain ke nameserver kami!

**Support:** @bukanaol
"""
        bot.send_message("@taskforce_store", status_message, parse_mode='Markdown')
    except Exception as e:
        logging.error(f"Error sending status update: {e}")

# Schedule status updates
schedule.every(4).hours.do(send_status_update)

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s",
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger()

def run_scheduler():
    """Run the scheduler in background."""
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    from termcolor import colored
    
    logger.info(colored("🚀 Bot Cloudflare Pro Starting...", 'green'))
    logger.info(colored("👨‍💻 Created by @bukanaol", 'blue'))
    logger.info(colored("🌐 Using Cloudflare API v4", 'cyan'))
    logger.info(colored("🎁 Domain donation system enabled", 'yellow'))
    
    # Start scheduler in background
    import threading
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    
    # Start bot
    try:
        logger.info(colored("✅ Bot started successfully!", 'green'))
        bot.polling(none_stop=True, timeout=60)
    except KeyboardInterrupt:
        logger.info(colored("🛑 Bot stopped by user", 'red'))
    except Exception as e:
        logger.error(colored(f"❌ Bot error: {e}", 'red'))