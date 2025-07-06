# RestoHub - Sistem Manajemen Restoran

RestoHub adalah sistem manajemen restoran berbasis web yang dibangun dengan Flask dan MongoDB. Sistem ini mendukung dua role pengguna: Admin dan Kasir dengan fitur-fitur yang sesuai dengan kebutuhan masing-masing.

## 🚀 Fitur Utama

### 👨‍💼 Admin
- ✅ Login/logout dengan session management
- ✅ CRUD data menu (makanan, minuman, snack)
- ✅ CRUD kasir (user dengan role kasir)
- ✅ Melihat seluruh transaksi semua kasir
- ✅ Dashboard dengan statistik lengkap
- ✅ Manajemen stok dan ketersediaan menu

### 👨‍💻 Kasir
- ✅ Login/logout dengan session management
- ✅ Melakukan transaksi (pilih item menu, jumlah, metode bayar)
- ✅ Melihat riwayat transaksi milik sendiri
- ✅ Toggle ketersediaan stok menu
- ✅ Manajemen shift kerja
- ✅ Dashboard dengan statistik personal

## 🛠️ Tech Stack

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **Flask-Login** - Session management & authentication
- **MongoDB** - Database NoSQL
- **MongoEngine** - ODM (Object Document Mapper)
- **bcrypt** - Password hashing

### Frontend
- **Tailwind CSS** - Styling framework (via CDN)
- **Jinja2** - Template engine
- **Font Awesome** - Icons
- **Vanilla JavaScript** - Interactive features

## 📦 Instalasi

### 1. Clone Repository
\`\`\`bash
git clone <repository-url>
cd restohub
\`\`\`

### 2. Install Dependencies
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 3. Setup MongoDB
Pastikan MongoDB sudah terinstall dan berjalan di sistem Anda:
\`\`\`bash
# Ubuntu/Debian
sudo systemctl start mongod

# macOS (dengan Homebrew)
brew services start mongodb-community

# Windows
# Jalankan MongoDB service dari Services atau command prompt
\`\`\`

### 4. Inisialisasi Database
\`\`\`bash
python scripts/init_data.py
\`\`\`

### 5. Jalankan Aplikasi
\`\`\`bash
python app.py
\`\`\`

Aplikasi akan berjalan di `http://localhost:5000`

## 👥 Default Login

### Admin
- **Username:** `admin`
- **Password:** `admin123`

### Kasir
- **Username:** `kasir1`
- **Password:** `kasir123`

## 📁 Struktur Project

\`\`\`
restohub/
├── app.py                 # Main application file
├── config.py             # Configuration settings
├── models.py             # Database models (MongoEngine)
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
├── blueprints/          # Flask blueprints
│   ├── __init__.py
│   ├── auth.py          # Authentication routes
│   ├── dashboard.py     # Dashboard routes
│   ├── menu.py          # Menu management routes
│   ├── transaksi.py     # Transaction routes
│   └── shift.py         # Shift management routes
├── templates/           # Jinja2 templates
│   ├── base.html        # Base template
│   ├── auth/
│   │   └── login.html
│   ├── dashboard/
│   │   ├── admin.html
│   │   └── kasir.html
│   ├── menu/
│   │   ├── list.html
│   │   ├── add.html
│   │   └── edit.html
│   ├── transaksi/
│   │   ├── new.html
│   │   ├── riwayat.html
│   │   └── detail.html
│   └── shift/
│       ├── start.html
│       └── riwayat.html
└── scripts/
    └── init_data.py     # Database initialization script
\`\`\`

## 🗄️ Database Schema

### Collections

#### Users
- `username` (String, unique)
- `password_hash` (String)
- `role` (String: 'admin' | 'kasir')
- `created_at` (DateTime)

#### MenuItems
- `nama` (String)
- `kategori` (String: 'makanan' | 'minuman' | 'snack')
- `harga` (Float)
- `stok` (Integer)
- `tersedia` (Boolean)
- `created_at` (DateTime)
- `updated_at` (DateTime)

#### Shifts
- `kasir` (Reference to User)
- `waktu_mulai` (DateTime)
- `waktu_selesai` (DateTime, optional)
- `is_active` (Boolean)
- `created_at` (DateTime)

#### Transaksi
- `kasir` (Reference to User)
- `shift` (Reference to Shift)
- `waktu` (DateTime)
- `metode_pembayaran` (String: 'cash' | 'qris')
- `total_harga` (Float)
- `created_at` (DateTime)

#### DetailTransaksi
- `transaksi` (Reference to Transaksi)
- `menu_item` (Reference to MenuItem)
- `jumlah` (Integer)
- `subtotal` (Float)
- `created_at` (DateTime)

## 🔐 Security Features

- ✅ Password hashing dengan bcrypt
- ✅ Session-based authentication
- ✅ Role-based access control
- ✅ CSRF protection (built-in Flask)
- ✅ Input validation dan sanitization
- ✅ Secure cookie configuration

## 🎨 UI/UX Features

- ✅ Responsive design (mobile-friendly)
- ✅ Modern UI dengan Tailwind CSS
- ✅ Interactive components dengan JavaScript
- ✅ Flash messages untuk feedback
- ✅ Loading states dan error handling
- ✅ Intuitive navigation

## 🚀 Production Deployment

### Environment Variables
\`\`\`bash
export SECRET_KEY="your-super-secret-key-here"
export MONGODB_DB="restohub_production"
export MONGODB_HOST="your-mongodb-host"
export MONGODB_PORT=27017
\`\`\`

### Recommended Production Setup
1. Use a production WSGI server (Gunicorn, uWSGI)
2. Set up reverse proxy (Nginx)
3. Use MongoDB Atlas or dedicated MongoDB server
4. Enable HTTPS/SSL
5. Set secure session cookies
6. Implement proper logging
7. Set up monitoring and backups

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

Jika Anda mengalami masalah atau memiliki pertanyaan:

1. Periksa dokumentasi ini
2. Cek MongoDB connection
3. Pastikan semua dependencies terinstall
4. Jalankan script inisialisasi database

## 🔄 Updates & Roadmap

### Planned Features
- [ ] Laporan penjualan dengan grafik
- [ ] Export data ke Excel/PDF
- [ ] Notifikasi stok menipis
- [ ] Multi-branch support
- [ ] API endpoints untuk mobile app
- [ ] Real-time updates dengan WebSocket

---

**RestoHub** - Solusi lengkap untuk manajemen restoran modern! 🍽️
