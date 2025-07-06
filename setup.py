"""
Script SIMPEL untuk setup RestoHub dengan MongoDB Atlas
Jalankan: python setup.py
"""

from mongoengine import connect
from models import User, MenuItem

# MongoDB Atlas URI
MONGODB_URI = 'mongodb+srv://adityagiri206:WShjLhbxMLv0LCR8@restohub-app.tsghcp7.mongodb.net/restohub?retryWrites=true&w=majority&appName=restohub-app'

def setup_restohub():
    print("🚀 Setting up RestoHub with MongoDB Atlas...")
    
    # Connect ke MongoDB Atlas
    try:
        connect(host=MONGODB_URI)
        print("✅ Connected to MongoDB Atlas!")
        print("🌐 Cluster: restohub-app.tsghcp7.mongodb.net")
    except Exception as e:
        print(f"❌ MongoDB Atlas connection failed: {e}")
        print("💡 Check your internet connection!")
        return
    
    # Buat admin user
    if not User.objects(username='admin').first():
        admin = User(username='admin', role='admin')
        admin.set_password('admin123')
        admin.save()
        print("✅ Admin created: admin/admin123")
    else:
        print("ℹ️  Admin already exists")
    
    # Buat kasir user  
    if not User.objects(username='kasir1').first():
        kasir = User(username='kasir1', role='kasir')
        kasir.set_password('kasir123')
        kasir.save()
        print("✅ Kasir created: kasir1/kasir123")
    else:
        print("ℹ️  Kasir already exists")
    
    # Buat sample menu
    menus = [
        {'nama': 'Nasi Goreng Spesial', 'kategori': 'makanan', 'harga': 25000, 'stok': 50},
        {'nama': 'Mie Ayam Bakso', 'kategori': 'makanan', 'harga': 20000, 'stok': 30},
        {'nama': 'Ayam Bakar', 'kategori': 'makanan', 'harga': 35000, 'stok': 20},
        {'nama': 'Gado-gado', 'kategori': 'makanan', 'harga': 18000, 'stok': 25},
        {'nama': 'Soto Ayam', 'kategori': 'makanan', 'harga': 22000, 'stok': 40},
        {'nama': 'Es Teh Manis', 'kategori': 'minuman', 'harga': 5000, 'stok': 100},
        {'nama': 'Es Jeruk', 'kategori': 'minuman', 'harga': 8000, 'stok': 80},
        {'nama': 'Kopi Hitam', 'kategori': 'minuman', 'harga': 10000, 'stok': 60},
        {'nama': 'Jus Alpukat', 'kategori': 'minuman', 'harga': 15000, 'stok': 30},
        {'nama': 'Air Mineral', 'kategori': 'minuman', 'harga': 3000, 'stok': 200},
        {'nama': 'Keripik Singkong', 'kategori': 'snack', 'harga': 12000, 'stok': 50},
        {'nama': 'Pisang Goreng', 'kategori': 'snack', 'harga': 8000, 'stok': 40},
        {'nama': 'Tahu Isi', 'kategori': 'snack', 'harga': 6000, 'stok': 60},
        {'nama': 'Bakwan Jagung', 'kategori': 'snack', 'harga': 5000, 'stok': 70},
    ]
    
    created = 0
    for menu in menus:
        if not MenuItem.objects(nama=menu['nama']).first():
            MenuItem(**menu).save()
            created += 1
    
    if created > 0:
        print(f"✅ Created {created} sample menus")
    else:
        print("ℹ️  Sample menus already exist")
    
    print("\n🎉 Setup complete!")
    print("☁️  Your data is stored in MongoDB Atlas cloud")
    print("🔑 Login info:")
    print("   Admin: admin / admin123")
    print("   Kasir: kasir1 / kasir123")
    print("\n▶️  Run: python app.py")

if __name__ == '__main__':
    setup_restohub()
