#controllers/role_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from models.role import Role

role_bp = Blueprint('role', __name__, url_prefix='/role')

@role_bp.route('/create_role', methods=['POST'])
@login_required
def create_role():
    role_name = request.form['role_name']
    role = Role(name=role_name)
    try:
        db.session.add(role)
        db.session.commit()
        flash("Role created successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error creating role: {str(e)}", "danger")
    
    return redirect(url_for('dashboard.dashboard'))

@role_bp.route('/roles')
@login_required
def list_roles():
    roles = Role.query.all()
    return render_template('role/list.html', roles=roles)

@role_bp.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    role = Role.query.get_or_404(id)
    
    if request.method == 'POST':
        role.name = request.form['role_name']
        
        try:
            db.session.commit()
            flash("Role updated successfully!", "success")
            return redirect(url_for('role.list_roles'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating role: {str(e)}", "danger")
    
    return render_template('role/edit.html', role=role)

@role_bp.route('/assign_roles/<int:id>')
@login_required
def assign_roles(id):
    role = Role.query.get_or_404(id)
    return render_template('role/assign.html', role=role)

@role_bp.route('/roles/delete/<int:id>', methods=['POST'])
@login_required
def delete_role(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    
    flash("Role deleted successfully!", "success")
    return redirect(url_for('role.list_roles'))

