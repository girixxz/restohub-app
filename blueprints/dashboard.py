from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models import User, MenuItem, Transaksi, Shift
from datetime import datetime, timedelta

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
@login_required
def index():
    if current_user.is_admin():
        return redirect(url_for('dashboard.admin'))
    else:
        return redirect(url_for('dashboard.kasir'))

@dashboard_bp.route('/admin')
@login_required
def admin():
    if not current_user.is_admin():
        return redirect(url_for('dashboard.kasir'))
    
    # Statistics untuk admin
    total_kasir = User.objects(role='kasir').count()
    total_menu = MenuItem.objects().count()
    total_transaksi_hari_ini = Transaksi.objects(
        waktu__gte=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    ).count()
    
    # Transaksi terbaru
    transaksi_terbaru = Transaksi.objects().order_by('-waktu').limit(5)
    
    # Current date
    current_date = datetime.now().strftime('%d %B %Y')
    
    return render_template('dashboard/admin.html', 
                         total_kasir=total_kasir,
                         total_menu=total_menu,
                         total_transaksi_hari_ini=total_transaksi_hari_ini,
                         transaksi_terbaru=transaksi_terbaru,
                         current_date=current_date)

@dashboard_bp.route('/kasir')
@login_required
def kasir():
    if not current_user.is_kasir():
        return redirect(url_for('dashboard.admin'))
    
    # Statistics untuk kasir
    shift_aktif = Shift.objects(kasir=current_user, is_active=True).first()
    transaksi_hari_ini = Transaksi.objects(
        kasir=current_user,
        waktu__gte=datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    ).count()
    
    # Transaksi terbaru kasir
    transaksi_terbaru = Transaksi.objects(kasir=current_user).order_by('-waktu').limit(5)
    
    return render_template('dashboard/kasir.html',
                         shift_aktif=shift_aktif,
                         transaksi_hari_ini=transaksi_hari_ini,
                         transaksi_terbaru=transaksi_terbaru)
