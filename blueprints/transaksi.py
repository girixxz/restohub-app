from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, make_response
from flask_login import login_required, current_user
from models import MenuItem, Transaksi, DetailTransaksi, Shift, User
from datetime import datetime
import csv
import io

transaksi_bp = Blueprint('transaksi', __name__)

@transaksi_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_transaksi():
    if not current_user.is_kasir():
        flash('Akses ditolak! Hanya kasir yang dapat melakukan transaksi.', 'error')
        return redirect(url_for('dashboard.index'))
    
    # Cek shift aktif
    shift_aktif = Shift.objects(kasir=current_user, is_active=True).first()
    if not shift_aktif:
        flash('Anda harus memulai shift terlebih dahulu!', 'warning')
        return redirect(url_for('shift.start_shift'))
    
    if request.method == 'POST':
        metode_pembayaran = request.form.get('metode_pembayaran')
        items = request.form.getlist('items')
        quantities = request.form.getlist('quantities')
        
        if not items or not quantities:
            flash('Pilih minimal satu item untuk transaksi!', 'error')
            return redirect(url_for('transaksi.new_transaksi'))
        
        try:
            # Buat transaksi baru
            transaksi = Transaksi(
                kasir=current_user,
                shift=shift_aktif,
                metode_pembayaran=metode_pembayaran,
                total_harga=0
            )
            transaksi.save()
            
            total_harga = 0
            
            # Buat detail transaksi
            for item_id, qty in zip(items, quantities):
                if qty and int(qty) > 0:
                    menu_item = MenuItem.objects(id=item_id).first()
                    if menu_item and menu_item.tersedia and menu_item.stok >= int(qty):
                        subtotal = menu_item.harga * int(qty)
                        
                        detail = DetailTransaksi(
                            transaksi=transaksi,
                            menu_item=menu_item,
                            jumlah=int(qty),
                            subtotal=subtotal
                        )
                        detail.save()
                        
                        # Update stok
                        menu_item.stok -= int(qty)
                        if menu_item.stok == 0:
                            menu_item.tersedia = False
                        menu_item.save()
                        
                        total_harga += subtotal
            
            # Update total harga transaksi
            transaksi.total_harga = total_harga
            transaksi.save()
            
            flash(f'Transaksi berhasil! Total: Rp {total_harga:,.0f}', 'success')
            return redirect(url_for('transaksi.riwayat'))
            
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    # Ambil menu yang tersedia
    menu_items = MenuItem.objects(tersedia=True, stok__gt=0).order_by('kategori', 'nama')
    return render_template('transaksi/new.html', menu_items=menu_items)

@transaksi_bp.route('/riwayat')
@login_required
def riwayat():
    # Get filter parameters
    tanggal = request.args.get('tanggal')
    kasir_id = request.args.get('kasir')
    
    # Build query untuk transaksi
    query = {}
    
    # Filter berdasarkan role
    if current_user.is_admin():
        # Admin bisa lihat semua transaksi
        pass
    else:
        # Kasir hanya bisa lihat transaksi sendiri
        query['kasir'] = current_user
    
    # Filter tanggal
    if tanggal:
        try:
            target_date = datetime.strptime(tanggal, '%Y-%m-%d')
            start_of_day = target_date.replace(hour=0, minute=0, second=0)
            end_of_day = target_date.replace(hour=23, minute=59, second=59)
            query['waktu__gte'] = start_of_day
            query['waktu__lte'] = end_of_day
        except ValueError:
            pass
    
    # Filter kasir (hanya untuk admin)
    if current_user.is_admin() and kasir_id:
        kasir = User.objects(id=kasir_id).first()
        if kasir:
            query['kasir'] = kasir
    
    # Get transaksi dengan filter
    transaksi_list = Transaksi.objects(**query).order_by('-waktu')
    
    # Siapkan data transaksi dengan detail items
    transaksi_data = []
    total_pendapatan = 0
    for transaksi in transaksi_list:
        detail_items = DetailTransaksi.objects(transaksi=transaksi)
        transaksi_data.append({
            'transaksi': transaksi,
            'detail_items': detail_items
        })
        total_pendapatan += transaksi.total_harga
    
    # Ambil list kasir untuk filter (hanya untuk admin)
    kasir_list = []
    if current_user.is_admin():
        kasir_list = User.objects(role='kasir').order_by('username')
    
    # Summary statistics
    summary = {
        'total_transaksi': len(transaksi_data),
        'total_pendapatan': total_pendapatan,
        'rata_rata': total_pendapatan / len(transaksi_data) if len(transaksi_data) > 0 else 0
    }
    
    return render_template('transaksi/riwayat.html', 
                         transaksi_data=transaksi_data,
                         kasir_list=kasir_list,
                         selected_tanggal=tanggal,
                         selected_kasir=kasir_id,
                         summary=summary)

@transaksi_bp.route('/detail/<transaksi_id>')
@login_required
def detail_transaksi(transaksi_id):
    transaksi = Transaksi.objects(id=transaksi_id).first()
    
    if not transaksi:
        flash('Transaksi tidak ditemukan!', 'error')
        return redirect(url_for('transaksi.riwayat'))
    
    # Kasir hanya bisa lihat transaksi sendiri
    if current_user.is_kasir() and transaksi.kasir != current_user:
        flash('Akses ditolak!', 'error')
        return redirect(url_for('transaksi.riwayat'))
    
    detail_list = DetailTransaksi.objects(transaksi=transaksi)
    
    return render_template('transaksi/detail.html', 
                         transaksi=transaksi, 
                         detail_list=detail_list)

@transaksi_bp.route('/download-csv')
@login_required
def download_csv():
    if not current_user.is_admin():
        flash('Akses ditolak! Hanya admin yang dapat download laporan.', 'error')
        return redirect(url_for('transaksi.riwayat'))
    
    # Get filter parameters
    tanggal = request.args.get('tanggal')
    kasir_id = request.args.get('kasir')
    
    # Build query untuk transaksi
    query = {}
    
    # Filter tanggal
    if tanggal:
        try:
            target_date = datetime.strptime(tanggal, '%Y-%m-%d')
            start_of_day = target_date.replace(hour=0, minute=0, second=0)
            end_of_day = target_date.replace(hour=23, minute=59, second=59)
            query['waktu__gte'] = start_of_day
            query['waktu__lte'] = end_of_day
        except ValueError:
            pass
    
    # Filter kasir
    if kasir_id:
        kasir = User.objects(id=kasir_id).first()
        if kasir:
            query['kasir'] = kasir
    
    # Get transaksi
    transaksi_list = Transaksi.objects(**query).order_by('-waktu')
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        'Tanggal',
        'Waktu',
        'Kasir',
        'Metode Pembayaran',
        'Total (Rp)',
        'Items',
        'Detail Items'
    ])
    
    # Data per transaksi
    for transaksi in transaksi_list:
        # Get detail items
        detail_items = DetailTransaksi.objects(transaksi=transaksi)
        
        # Create items summary
        items_summary = []
        items_detail = []
        
        for detail in detail_items:
            items_summary.append(f"{detail.menu_item.nama} x{detail.jumlah}")
            items_detail.append(f"{detail.menu_item.nama} x{detail.jumlah} = Rp{detail.subtotal:,.0f}")
        
        writer.writerow([
            transaksi.waktu.strftime('%Y-%m-%d'),
            transaksi.waktu.strftime('%H:%M:%S'),
            transaksi.kasir.username,
            transaksi.metode_pembayaran.upper(),
            f"{transaksi.total_harga:,.0f}",
            ', '.join(items_summary),
            ' | '.join(items_detail)
        ])
    
    # Create response
    output.seek(0)
    response = make_response(output.getvalue())
    response.headers['Content-Type'] = 'text/csv'
    response.headers['Content-Disposition'] = f'attachment; filename=laporan_transaksi_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
    
    return response
