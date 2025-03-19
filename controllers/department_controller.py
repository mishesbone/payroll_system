#controllers/deparment_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user    
from app import db
from controllers.dashboard_controller import user_belongs_to_company
from models.department import Department


department_bp = Blueprint('department', __name__, url_prefix='/department')

@department_bp.route('/create_department', methods=['POST'])
@login_required
@user_belongs_to_company
def create_department():
    department_name = request.form['department_name']
    department = Department(name=department_name)
    try:
        db.session.add(department)
        db.session.commit()
        flash("Department created successfully!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Error creating department: {str(e)}", "danger")
    
    return redirect(url_for('dashboard.dashboard'))


@department_bp.route('/departments')
@login_required
@user_belongs_to_company
def list_departments():
    departments = Department.query.all()
    return render_template('department/list.html', departments=departments)

@department_bp.route('/departments/edit/<int:id>', methods=['GET', 'POST'])
@login_required
@user_belongs_to_company
def edit_department(id):
    department = Department.query.get_or_404(id)
    
    if request.method == 'POST':
        department.name = request.form['department_name']
        
        try:
            db.session.commit()
            flash("Department updated successfully!", "success")
            return redirect(url_for('department.list_departments'))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating department: {str(e)}", "danger")
    
    return render_template('department/edit.html', department=department)


@department_bp.route('/departments/<int:id>')
@login_required
@user_belongs_to_company
def profile_department(id):
    department = Department.query.get_or_404(id)
    return render_template('department/profile.html', department=department)

@department_bp.route('/departments/delete/<int:id>', methods=['POST'])
@login_required
@user_belongs_to_company
def delete_department(id):
    department = Department.query.get_or_404(id)
    db.session.delete(department)
    db.session.commit()
    
    flash("Department deleted successfully!", "success")
    return redirect(url_for('department.list_departments'))

@department_bp.route('/departments/export', methods=['GET'])
@login_required
@user_belongs_to_company
def export_departments():
    departments = Department.query.all()
    # Logic to export departments to CSV
    return jsonify({"message": "Exporting departments to CSV"})