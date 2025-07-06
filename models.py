from mongoengine import Document, StringField, FloatField, IntField, BooleanField, DateTimeField, ReferenceField, ListField
from flask_login import UserMixin
from datetime import datetime
import bcrypt

class User(Document, UserMixin):
    username = StringField(required=True, unique=True, max_length=50)
    password_hash = StringField(required=True)
    role = StringField(required=True, choices=['admin', 'kasir'])
    created_at = DateTimeField(default=datetime.utcnow)
    
    def set_password(self, password):
        """Hash dan simpan password"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def check_password(self, password):
        """Verifikasi password"""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_kasir(self):
        return self.role == 'kasir'
    
    meta = {
        'collection': 'users',
        'indexes': ['username']
    }

class MenuItem(Document):
    nama = StringField(required=True, max_length=100)
    kategori = StringField(required=True, choices=['makanan', 'minuman', 'snack'])
    harga = FloatField(required=True, min_value=0)
    stok = IntField(required=True, min_value=0)
    tersedia = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    updated_at = DateTimeField(default=datetime.utcnow)
    
    def save(self, *args, **kwargs):
        self.updated_at = datetime.utcnow()
        return super().save(*args, **kwargs)
    
    meta = {
        'collection': 'menu_items',
        'indexes': ['kategori', 'tersedia']
    }

class Shift(Document):
    kasir = ReferenceField(User, required=True)
    waktu_mulai = DateTimeField(required=True)
    waktu_selesai = DateTimeField()
    is_active = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'shifts',
        'indexes': ['kasir', 'is_active', 'waktu_mulai']
    }

class Transaksi(Document):
    kasir = ReferenceField(User, required=True)
    shift = ReferenceField(Shift, required=True)
    waktu = DateTimeField(default=datetime.utcnow)
    metode_pembayaran = StringField(required=True, choices=['cash', 'qris'])
    total_harga = FloatField(required=True, min_value=0)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'transaksi',
        'indexes': ['kasir', 'shift', 'waktu']
    }

class DetailTransaksi(Document):
    transaksi = ReferenceField(Transaksi, required=True)
    menu_item = ReferenceField(MenuItem, required=True)
    jumlah = IntField(required=True, min_value=1)
    subtotal = FloatField(required=True, min_value=0)
    created_at = DateTimeField(default=datetime.utcnow)
    
    meta = {
        'collection': 'detail_transaksi',
        'indexes': ['transaksi']
    }
