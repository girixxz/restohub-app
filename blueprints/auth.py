from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('dashboard.admin'))
        else:
            return redirect(url_for('dashboard.kasir'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username dan password harus diisi!', 'error')
            return render_template('auth/login.html')
        
        user = User.objects(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash(f'Selamat datang, {user.username}!', 'success')
            
            # Redirect berdasarkan role
            if user.is_admin():
                return redirect(url_for('dashboard.admin'))
            else:
                return redirect(url_for('dashboard.kasir'))
        else:
            flash('Username atau password salah!', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    username = current_user.username
    logout_user()
    flash(f'Sampai jumpa, {username}!', 'info')
    return redirect(url_for('auth.login'))
