from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import MenuItem
from bson import ObjectId

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/')
@login_required
def list_menu():
    kategori_filter = request.args.get('kategori', '')
    
    if kategori_filter:
        menu_items = MenuItem.objects(kategori=kategori_filter).order_by('nama')
    else:
        menu_items = MenuItem.objects().order_by('kategori', 'nama')
    
    return render_template('menu/list.html', menu_items=menu_items, kategori_filter=kategori_filter)

@menu_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_menu():
    if not current_user.is_admin():
        flash('Akses ditolak! Hanya admin yang dapat menambah menu.', 'error')
        return redirect(url_for('menu.list_menu'))
    
    if request.method == 'POST':
        nama = request.form.get('nama')
        kategori = request.form.get('kategori')
        harga = request.form.get('harga')
        stok = request.form.get('stok')
        
        try:
            menu_item = MenuItem(
                nama=nama,
                kategori=kategori,
                harga=float(harga),
                stok=int(stok),
                tersedia=True
            )
            menu_item.save()
            flash(f'Menu "{nama}" berhasil ditambahkan!', 'success')
            return redirect(url_for('menu.list_menu'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('menu/add.html')

@menu_bp.route('/edit/<menu_id>', methods=['GET', 'POST'])
@login_required
def edit_menu(menu_id):
    if not current_user.is_admin():
        flash('Akses ditolak! Hanya admin yang dapat mengedit menu.', 'error')
        return redirect(url_for('menu.list_menu'))
    
    menu_item = MenuItem.objects(id=menu_id).first()
    if not menu_item:
        flash('Menu tidak ditemukan!', 'error')
        return redirect(url_for('menu.list_menu'))
    
    if request.method == 'POST':
        menu_item.nama = request.form.get('nama')
        menu_item.kategori = request.form.get('kategori')
        menu_item.harga = float(request.form.get('harga'))
        menu_item.stok = int(request.form.get('stok'))
        
        try:
            menu_item.save()
            flash(f'Menu "{menu_item.nama}" berhasil diupdate!', 'success')
            return redirect(url_for('menu.list_menu'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('menu/edit.html', menu_item=menu_item)

@menu_bp.route('/delete/<menu_id>', methods=['POST'])
@login_required
def delete_menu(menu_id):
    if not current_user.is_admin():
        flash('Akses ditolak! Hanya admin yang dapat menghapus menu.', 'error')
        return redirect(url_for('menu.list_menu'))
    
    menu_item = MenuItem.objects(id=menu_id).first()
    if menu_item:
        nama = menu_item.nama
        menu_item.delete()
        flash(f'Menu "{nama}" berhasil dihapus!', 'success')
    else:
        flash('Menu tidak ditemukan!', 'error')
    
    return redirect(url_for('menu.list_menu'))

@menu_bp.route('/toggle-availability/<menu_id>', methods=['POST'])
@login_required
def toggle_availability(menu_id):
    menu_item = MenuItem.objects(id=menu_id).first()
    if not menu_item:
        return jsonify({'success': False, 'message': 'Menu tidak ditemukan'})
    
    menu_item.tersedia = not menu_item.tersedia
    menu_item.save()
    
    status = 'tersedia' if menu_item.tersedia else 'tidak tersedia'
    return jsonify({
        'success': True, 
        'message': f'Menu "{menu_item.nama}" sekarang {status}',
        'tersedia': menu_item.tersedia
    })
