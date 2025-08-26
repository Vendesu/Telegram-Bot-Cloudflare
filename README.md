# 🤖 Bot Cloudflare Pro - Telegram Bot untuk Manajemen Subdomain

**Versi Terbaru:** 2.0.0  
**Dibuat oleh:** [@bukanaol](https://t.me/bukanaol)  
**Update Channel:** [@codeplanetch](https://t.me/codeplanetch)  
**Grup Support:** [@codeplanethelper](https://t.me/codeplanethelper)

## 🎯 Deskripsi

Bot Cloudflare Pro adalah bot Telegram canggih yang memudahkan pembuatan dan pengelolaan subdomain di Cloudflare. Bot ini telah diperbarui dengan fitur terbaru Cloudflare API v4 dan sistem donasi domain untuk komunitas.

## ✨ Fitur Utama

### 🚀 **Manajemen Subdomain**
- ✅ Pembuatan subdomain otomatis dengan nama yang bermakna
- ✅ Validasi IP address yang canggih
- ✅ Pengelolaan subdomain yang sudah ada
- ✅ Integrasi dengan Cloudflare API v4 terbaru

### 🎁 **Sistem Donasi Domain**
- 🌐 Donasi domain yang tidak terpakai
- 📋 Tracking dan monitoring donasi

### 🔒 **Keamanan & Monitoring**
- 🔐 Enkripsi data sensitif
- 🛡️ Rate limiting untuk mencegah abuse
- 📊 Monitoring status bot real-time
- 💾 Sistem backup otomatis

### 🎨 **Interface Modern**
- ⌨️ Keyboard yang intuitif
- 📱 Responsive design
- 🎯 Navigasi yang mudah
- 🌈 Emoji dan formatting yang menarik

## 🚀 Fitur Terbaru v2.0.0

- **Cloudflare API v4**: Menggunakan API terbaru Cloudflare
- **Sistem Donasi**: Platform donasi domain untuk komunitas
- **Rate Limiting**: Pembatasan request untuk keamanan
- **Auto Backup**: Backup otomatis setiap 24 jam
- **Monitoring**: Status monitoring real-time
- **Security**: Enkripsi dan validasi input yang ditingkatkan

## 📋 Persyaratan Sistem

- **Python:** 3.8 atau lebih tinggi
- **OS:** Linux, Windows, macOS
- **Memory:** Minimal 512MB RAM
- **Storage:** Minimal 100MB free space
- **Internet:** Koneksi internet stabil

## 🛠️ Instalasi

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/bot-cloudflare-pro.git
cd bot-cloudflare-pro
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup Environment
Jalankan bot untuk pertama kali:
```bash
python3 botcf.py
```

Bot akan meminta informasi berikut:
- **Token Telegram Bot** (dari @BotFather)
- **Domain Default** (domain utama Anda)
- **Cloudflare API Token** (dari Cloudflare Dashboard)
- **Cloudflare Zone ID** (ID zona domain Anda)
- **Channel ID** (ID channel untuk notifikasi)
- **Donation Channel ID** (ID channel untuk donasi)

### 4. Konfigurasi Cloudflare

#### Membuat API Token:
1. Login ke [Cloudflare Dashboard](https://dash.cloudflare.com/)
2. Buka **My Profile** → **API Tokens**
3. Klik **Create Token**
4. Pilih **Custom token**
5. Berikan permission:
   - **Zone:Zone:Read**
   - **Zone:DNS:Edit**
6. Pilih zone yang sesuai
7. Copy token yang dihasilkan

#### Mendapatkan Zone ID:
1. Buka domain Anda di Cloudflare Dashboard
2. Zone ID ada di sidebar kanan

## 🎮 Cara Penggunaan

### Perintah Dasar
- `/start` - Memulai bot dan menampilkan menu utama
- `/help` - Menampilkan bantuan lengkap
- `/add` - Membuat subdomain (alternatif)

### Menu Utama
- **🚀 Buat Subdomain** - Membuat subdomain baru
- **💾 Subdomain Saya** - Lihat subdomain yang sudah dibuat
- **🎁 Donasi Domain** - Sistem donasi domain
- **📊 Status Bot** - Status bot dan layanan
- **ℹ️ Bantuan** - Panduan penggunaan
- **👨‍💻 Owner** - Informasi owner

### Membuat Subdomain
1. Klik **🚀 Buat Subdomain**
2. Masukkan IP address yang valid
3. Bot akan membuat subdomain otomatis
4. Subdomain siap digunakan dalam 1-5 menit

### Sistem Donasi
1. Klik **🎁 Donasi Domain**
2. Pilih jenis donasi:
   - 🌐 Donasi Domain
   - 📋 Lihat Donasi
3. Ikuti instruksi yang diberikan

## 🔧 Konfigurasi Lanjutan

### File Konfigurasi
Bot menggunakan file `.env` untuk konfigurasi:
```env
TELEGRAM_TOKEN=your_bot_token
DEFAULT_DOMAIN=yourdomain.com
CLOUDFLARE_API_TOKEN=your_api_token
CLOUDFLARE_ZONE_ID=your_zone_id
CHANNEL_ID=@your_channel
DONATION_CHANNEL_ID=@donation_channel
ENCRYPTION_KEY=auto_generated_key
```

### Customization
Edit file `config.py` untuk mengubah:
- Nama bot dan versi
- Rate limiting
- Backup settings
- Monitoring configuration

## 📊 Monitoring & Logs

### Log Files
- `bot.log` - Log utama bot
- `backups/` - File backup otomatis

### Status Monitoring
Bot mengirim status update setiap 4 jam ke channel yang ditentukan.

## 🔒 Keamanan

- **Rate Limiting**: Pembatasan request per user
- **Input Validation**: Validasi semua input user
- **Encryption**: Enkripsi data sensitif
- **Sanitization**: Pembersihan input untuk mencegah injection

## 🚨 Troubleshooting

### Masalah Umum

#### Bot tidak merespon
- Cek koneksi internet
- Pastikan token bot valid
- Cek log file untuk error

#### Gagal membuat subdomain
- Pastikan IP address valid
- Cek Cloudflare API token
- Verifikasi Zone ID

#### Error Cloudflare API
- Cek permission API token
- Pastikan domain aktif di Cloudflare
- Cek rate limit Cloudflare

### Log dan Debug
```bash
# Lihat log real-time
tail -f bot.log

# Restart bot
pkill -f botcf.py
python3 botcf.py
```

## 🤝 Kontribusi

Kontribusi sangat diterima! Silakan:
1. Fork repository
2. Buat feature branch
3. Commit perubahan
4. Push ke branch
5. Buat Pull Request

## 📞 Support

- **Owner:** [@bukanaol](https://t.me/bukanaol)
- **Channel:** [@codeplanetch](https://t.me/codeplanetch)
- **Group:** [@codeplanethelper](https://t.me/codeplanethelper)
- **Email:** bukanaol@example.com

## 📄 Lisensi

Kode ini dirilis di bawah lisensi MIT. Lihat file `LICENSE` untuk detail lebih lanjut.

## 🙏 Ucapan Terima Kasih

Terima kasih kepada:
- Cloudflare untuk API yang luar biasa
- Telegram untuk platform bot yang hebat
- Komunitas yang telah berkontribusi
- Semua user yang telah menggunakan bot ini

## 🔄 Changelog

### v2.0.0 (Latest)
- ✨ Sistem donasi domain
- 🔄 Cloudflare API v4
- 🛡️ Rate limiting dan security
- 📊 Monitoring real-time
- 💾 Auto backup system
- 🎨 Interface modern

### v1.0.0
- 🚀 Fitur dasar pembuatan subdomain
- 🔗 Integrasi Cloudflare API
- 📱 Bot Telegram sederhana

---

**⭐ Jangan lupa star repository ini jika bermanfaat!**  
**🔄 Update terbaru selalu di channel @codeplanetch**
