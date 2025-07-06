from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import Shift
from datetime import datetime

shift_bp = Blueprint('shift', __name__)

@shift_bp.route('/start', methods=['GET', 'POST'])
@login_required
def start_shift():
    if not current_user.is_kasir():
        flash('Akses ditolak! Hanya kasir yang dapat memulai shift.', 'error')
        return redirect(url_for('dashboard.index'))
    
    # Cek apakah sudah ada shift aktif
    shift_aktif = Shift.objects(kasir=current_user, is_active=True).first()
    if shift_aktif:
        flash('Anda sudah memiliki shift aktif!', 'warning')
        return redirect(url_for('dashboard.kasir'))
    
    if request.method == 'POST':
        shift = Shift(
            kasir=current_user,
            waktu_mulai=datetime.now(),
            is_active=True
        )
        shift.save()
        flash('Shift berhasil dimulai!', 'success')
        return redirect(url_for('dashboard.kasir'))
    
    # Kirim current_time ke template
    current_time = datetime.now().strftime('%d %B %Y, %H:%M')
    return render_template('shift/start.html', current_time=current_time)

@shift_bp.route('/end', methods=['POST'])
@login_required
def end_shift():
    if not current_user.is_kasir():
        flash('Akses ditolak!', 'error')
        return redirect(url_for('dashboard.index'))
    
    shift_aktif = Shift.objects(kasir=current_user, is_active=True).first()
    if not shift_aktif:
        flash('Tidak ada shift aktif!', 'warning')
        return redirect(url_for('dashboard.kasir'))
    
    shift_aktif.waktu_selesai = datetime.now()
    shift_aktif.is_active = False
    shift_aktif.save()
    
    flash('Shift berhasil diakhiri!', 'success')
    return redirect(url_for('dashboard.kasir'))

@shift_bp.route('/riwayat')
@login_required
def riwayat():
    if current_user.is_admin():
        shifts = Shift.objects().order_by('-waktu_mulai')
    else:
        shifts = Shift.objects(kasir=current_user).order_by('-waktu_mulai')
    
    return render_template('shift/riwayat.html', shifts=shifts)
