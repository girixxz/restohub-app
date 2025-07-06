"""
Script alternatif untuk inisialisasi database RestoHub
Letakkan file ini di root directory dan jalankan: python init_db.py
"""

from mongoengine import connect
from models import User, MenuItem

def init_database():
    try:
        # Connect to MongoDB
        connect('restohub', host='localhost', port=27017)
        
        print("🔄 Menginisialisasi database RestoHub...")
        
        # Create admin user
        admin_user = User.objects(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin', role='admin')
            admin_user.set_password('admin123')
            admin_user.save()
            print("✅ Admin user berhasil dibuat (username: admin, password: admin123)")
        else:
            print("ℹ️  Admin user sudah ada")
        
        # Create kasir user
        kasir_user = User.objects(username='kasir1').first()
        if not kasir_user:
            kasir_user = User(username='kasir1', role='kasir')
            kasir_user.set_password('kasir123')
            kasir_user.save()
            print("✅ Kasir user berhasil dibuat (username: kasir1, password: kasir123)")
        else:
            print("ℹ️  Kasir user sudah ada")
        
        # Create sample menu items
        sample_menus = [
            # Makanan
            {'nama': 'Nasi Goreng Spesial', 'kategori': 'makanan', 'harga': 25000, 'stok': 50},
            {'nama': 'Mie Ayam Bakso', 'kategori': 'makanan', 'harga': 20000, 'stok': 30},
            {'nama': 'Ayam Bakar', 'kategori': 'makanan', 'harga': 35000, 'stok': 20},
            {'nama': 'Gado-gado', 'kategori': 'makanan', 'harga': 18000, 'stok': 25},
            {'nama': 'Soto Ayam', 'kategori': 'makanan', 'harga': 22000, 'stok': 40},
            
            # Minuman
            {'nama': 'Es Teh Manis', 'kategori': 'minuman', 'harga': 5000, 'stok': 100},
            {'nama': 'Es Jeruk', 'kategori': 'minuman', 'harga': 8000, 'stok': 80},
            {'nama': 'Kopi Hitam', 'kategori': 'minuman', 'harga': 10000, 'stok': 60},
            {'nama': 'Jus Alpukat', 'kategori': 'minuman', 'harga': 15000, 'stok': 30},
            {'nama': 'Air Mineral', 'kategori': 'minuman', 'harga': 3000, 'stok': 200},
            
            # Snack
            {'nama': 'Keripik Singkong', 'kategori': 'snack', 'harga': 12000, 'stok': 50},
            {'nama': 'Pisang Goreng', 'kategori': 'snack', 'harga': 8000, 'stok': 40},
            {'nama': 'Tahu Isi', 'kategori': 'snack', 'harga': 6000, 'stok': 60},
            {'nama': 'Bakwan Jagung', 'kategori': 'snack', 'harga': 5000, 'stok': 70},
        ]
        
        menu_created = 0
        for menu_data in sample_menus:
            existing_menu = MenuItem.objects(nama=menu_data['nama']).first()
            if not existing_menu:
                menu_item = MenuItem(**menu_data)
                menu_item.save()
                menu_created += 1
        
        if menu_created > 0:
            print(f"✅ {menu_created} menu contoh berhasil dibuat")
        else:
            print("ℹ️  Menu contoh sudah ada")
        
        print("\n🎉 Inisialisasi database selesai!")
        print("\n📋 Informasi Login:")
        print("   Admin - username: admin, password: admin123")
        print("   Kasir - username: kasir1, password: kasir123")
        print("\n🚀 Jalankan aplikasi dengan: python app.py")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        print("\n🔍 Troubleshooting:")
        print("1. Pastikan MongoDB sudah berjalan")
        print("2. Pastikan semua dependencies sudah terinstall: pip install -r requirements.txt")
        print("3. Cek koneksi MongoDB di localhost:27017")

if __name__ == '__main__':
    init_database()
