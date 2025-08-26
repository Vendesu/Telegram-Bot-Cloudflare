# Configuration file for Telegram Bot Cloudflare Pro
# Created by @bukanaol

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot Configuration
BOT_TOKEN = os.getenv('TELEGRAM_TOKEN')
BOT_NAME = "Cloudflare Pro Bot"
BOT_VERSION = "2.0.0"
BOT_OWNER = "@bukanaol"

# Cloudflare Configuration
CLOUDFLARE_API_TOKEN = os.getenv('CLOUDFLARE_API_TOKEN')
CLOUDFLARE_ZONE_ID = os.getenv('CLOUDFLARE_ZONE_ID')
DEFAULT_DOMAIN = os.getenv('DEFAULT_DOMAIN')

# Channel Configuration
CHANNEL_ID = os.getenv('CHANNEL_ID')
DONATION_CHANNEL_ID = os.getenv('DONATION_CHANNEL_ID')

# Security Configuration
ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY')

# Bot Features Configuration
ENABLE_DONATION_SYSTEM = True
ENABLE_SUBDOMAIN_MANAGEMENT = True
ENABLE_STATUS_MONITORING = True
ENABLE_AUTO_BACKUP = True

# Subdomain Configuration
SUBDOMAIN_PREFIXES = [
    "fast", "secure", "reliable", "swift", "powerful", 
    "efficient", "smart", "dynamic", "rapid", "stable"
]

SUBDOMAIN_SUFFIXES = [
    "server", "node", "host", "instance", "service", 
    "app", "api", "gateway", "proxy", "cdn"
]

# Validation Rules
MAX_SUBDOMAIN_LENGTH = 63
MIN_SUBDOMAIN_LENGTH = 3
ALLOWED_SUBDOMAIN_CHARS = r"^[a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]$"

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s] %(message)s"
LOG_FILE = "bot.log"

# Schedule Configuration
STATUS_UPDATE_INTERVAL = 4  # hours
BACKUP_INTERVAL = 24  # hours

# Error Messages
ERROR_MESSAGES = {
    "invalid_ip": "❌ IP address tidak valid! Format yang benar: 192.168.1.1",
    "invalid_domain": "❌ Domain tidak valid! Format yang benar: example.com",
    "cloudflare_error": "❌ Terjadi kesalahan pada Cloudflare API",
    "network_error": "❌ Terjadi kesalahan jaringan",
    "permission_error": "❌ Anda tidak memiliki izin untuk melakukan ini",
    "rate_limit": "❌ Terlalu banyak request. Silakan tunggu beberapa saat"
}

# Success Messages
SUCCESS_MESSAGES = {
    "subdomain_created": "✅ Subdomain berhasil dibuat!",
    "donation_received": "🎁 Terima kasih atas donasi domain!",
    "backup_completed": "💾 Backup berhasil dibuat",
    "status_updated": "📊 Status berhasil diperbarui"
}

# Help Messages
HELP_SECTIONS = {
    "general": "Bot untuk membuat dan mengelola subdomain di Cloudflare",
    "commands": "Gunakan keyboard atau ketik /help untuk bantuan",
    "donation": "Sistem donasi domain untuk komunitas",
    "support": "Hubungi @bukanaol untuk support"
}

# Donation System Configuration
DONATION_TYPES = {
    "domain": "🌐 Donasi Domain",
    "money": "💰 Donasi Uang",
    "server": "🚀 Donasi Server/VPS"
}

DONATION_STATUSES = {
    "pending": "⏳ Pending Review",
    "approved": "✅ Disetujui",
    "rejected": "❌ Ditolak",
    "completed": "🎉 Selesai"
}

# API Endpoints (for future use)
API_ENDPOINTS = {
    "cloudflare_dns": "https://api.cloudflare.com/client/v4/zones/{zone_id}/dns_records",
    "cloudflare_zones": "https://api.cloudflare.com/client/v4/zones",
    "bot_api": "https://api.telegram.org/bot{token}"
}

# Feature Flags
FEATURES = {
    "auto_subdomain_naming": True,
    "domain_validation": True,
    "donation_system": True,
    "status_monitoring": True,
    "auto_backup": True,
    "rate_limiting": True,
    "user_management": True
}

# Rate Limiting
RATE_LIMITS = {
    "subdomain_creation": {"requests": 10, "window": 3600},  # 10 per hour
    "donation_submission": {"requests": 5, "window": 86400},  # 5 per day
    "status_check": {"requests": 20, "window": 3600}  # 20 per hour
}

# Backup Configuration
BACKUP_CONFIG = {
    "enabled": True,
    "interval_hours": 24,
    "max_backups": 7,
    "backup_dir": "backups/",
    "include_files": ["bot.log", "user_data.json"]
}

# Monitoring Configuration
MONITORING_CONFIG = {
    "enabled": True,
    "check_interval_minutes": 5,
    "alert_threshold": 3,  # consecutive failures
    "notification_channels": [CHANNEL_ID, DONATION_CHANNEL_ID]
}