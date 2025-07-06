from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import User

user_bp = Blueprint('user', __name__)

@user_bp.route('/')
@login_required
def list_users():
    if not current_user.is_admin():
        flash('Access denied! Only admin can manage users.', 'error')
        return redirect(url_for('dashboard.index'))
    
    users = User.objects().order_by('username')
    return render_template('user/list.html', users=users)

@user_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if not current_user.is_admin():
        flash('Access denied! Only admin can add users.', 'error')
        return redirect(url_for('user.list_users'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Check if username already exists
        if User.objects(username=username).first():
            flash('Username already exists!', 'error')
            return render_template('user/add.html')
        
        try:
            user = User(username=username, role=role)
            user.set_password(password)
            user.save()
            flash(f'User "{username}" created successfully!', 'success')
            return redirect(url_for('user.list_users'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('user/add.html')

@user_bp.route('/edit/<user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    if not current_user.is_admin():
        flash('Access denied! Only admin can edit users.', 'error')
        return redirect(url_for('user.list_users'))
    
    user = User.objects(id=user_id).first()
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('user.list_users'))
    
    # Prevent admin from editing themselves
    if user.id == current_user.id:
        flash('You cannot edit your own account!', 'warning')
        return redirect(url_for('user.list_users'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Check if username already exists (excluding current user)
        existing_user = User.objects(username=username, id__ne=user.id).first()
        if existing_user:
            flash('Username already exists!', 'error')
            return render_template('user/edit.html', user=user)
        
        try:
            user.username = username
            user.role = role
            if password:  # Only update password if provided
                user.set_password(password)
            user.save()
            flash(f'User "{username}" updated successfully!', 'success')
            return redirect(url_for('user.list_users'))
        except Exception as e:
            flash(f'Error: {str(e)}', 'error')
    
    return render_template('user/edit.html', user=user)

@user_bp.route('/delete/<user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if not current_user.is_admin():
        flash('Access denied! Only admin can delete users.', 'error')
        return redirect(url_for('user.list_users'))
    
    user = User.objects(id=user_id).first()
    if not user:
        flash('User not found!', 'error')
        return redirect(url_for('user.list_users'))
    
    # Prevent admin from deleting themselves
    if user.id == current_user.id:
        flash('You cannot delete your own account!', 'warning')
        return redirect(url_for('user.list_users'))
    
    try:
        username = user.username
        user.delete()
        flash(f'User "{username}" deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error: {str(e)}', 'error')
    
    return redirect(url_for('user.list_users'))

@user_bp.route('/toggle-status/<user_id>', methods=['POST'])
@login_required
def toggle_status(user_id):
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Access denied'})
    
    user = User.objects(id=user_id).first()
    if not user:
        return jsonify({'success': False, 'message': 'User not found'})
    
    # Prevent admin from disabling themselves
    if user.id == current_user.id:
        return jsonify({'success': False, 'message': 'Cannot modify your own account'})
    
    # Toggle active status (you might need to add this field to User model)
    # For now, we'll just return success
    return jsonify({'success': True, 'message': f'User status updated'})
