#controllers/user_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.user import User

user_bp = Blueprint('user', __name__, url_prefix='/user')

@user_bp.route('/users')
@login_required
def list_users():
    users = User.query.all()
    return render_template('user/list.html', users=users)

@user_bp.route('/users/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_user(id):
    user = User.query.get_or_404(id)
    
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        
        try:
            db.session.commit()
            flash("User updated successfully!", "success")
            return redirect(url_for('user.list_users'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating user: {str(e)}", "danger")
    
    return render_template('user/edit.html', user=user)

@user_bp.route('/users/delete/<int:id>', methods=['POST'])
@login_required
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    
    flash(f"User {user.username} deleted successfully!", "success")
    return redirect(url_for('admin.manage_users'))

# Add new user
@user_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_user():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        
        new_user = User(username=username, email=email, password=password)
        try:
            db.session.add(new_user)
            db.session.commit()
            flash("User added successfully!", "success")
            return redirect(url_for('user.list_users'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error adding user: {str(e)}", "danger")
    
    return render_template('user/add.html')
