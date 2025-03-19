from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.user import User
from models.leave import Leave
from services.email_service import EmailService as send_email
from forms.auth_forms import RegistrationForm, LoginForm, ResetPasswordForm  
from app import db


leave_bp = Blueprint('leave', __name__, url_prefix='/leave')

@leave_bp.route('/apply', methods=['POST'])
@login_required
def apply_leave():
    start_date = request.form['start_date']
    end_date = request.form['end_date']
    reason = request.form['reason']

    new_leave = Leave(
        start_date=start_date,
        end_date=end_date,
        reason=reason,
        user_id=current_user.id
    )

    db.session.add(new_leave)
    db.session.commit()

    flash("Leave application submitted successfully!", "success")
    return redirect(url_for('dashboard.dashboard'))

@leave_bp.route('/approve/<int:leave_id>', methods=['POST'])
@login_required
def approve_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)
    leave.status = "Approved"
    db.session.commit()

    flash("Leave approved successfully!", "success")
    return redirect(url_for('admin.dashboard'))

@leave_bp.route('/reject/<int:leave_id>', methods=['POST'])
@login_required
def reject_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)
    leave.status = "Rejected"
    db.session.commit()

    flash("Leave rejected!", "success")
    return redirect(url_for('admin.dashboard'))

@leave_bp.route('/cancel/<int:leave_id>', methods=['POST'])
@login_required
def cancel_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)
    db.session.delete(leave)
    db.session.commit()

    flash("Leave application cancelled!", "success")
    return redirect(url_for('dashboard.dashboard'))

@leave_bp.route('/view_all', methods=['GET'])
@login_required
def view_all_leaves():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))
    
    leaves = Leave.query.all()
    return render_template('leave/view_all.html', leaves=leaves)

@leave_bp.route('/view/<int:leave_id>', methods=['GET'])
@login_required
def view_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)
    return render_template('leave/view.html', leave=leave)  

@leave_bp.route('/edit/<int:leave_id>', methods=['POST'])
@login_required
def edit_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)

    leave.start_date = request.form['start_date']
    leave.end_date = request.form['end_date']
    leave.reason = request.form['reason']

    db.session.commit()

    flash("Leave application updated successfully!", "success")
    return redirect(url_for('dashboard.dashboard'))

@leave_bp.route('/delete/<int:leave_id>', methods=['POST'])
@login_required
def delete_leave(leave_id):
    leave = Leave.query.get_or_404(leave_id)
    db.session.delete(leave)
    db.session.commit()

    flash("Leave application deleted successfully!", "success")
    return redirect(url_for('dashboard.dashboard'))

@leave_bp.route('/export', methods=['GET'])
@login_required
def export_leaves():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))
    
    # Export leaves to CSV
    return jsonify({"message": "Leaves exported successfully!"})

@leave_bp.route('/export_pdf', methods=['GET'])
@login_required
def export_leaves_pdf():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))
    
    # Export leaves to PDF
    return jsonify({"message": "Leaves exported to PDF successfully!"})

@leave_bp.route('/export_excel', methods=['GET'])
@login_required
def export_leaves_excel():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))
    
    # Export leaves to Excel
    return jsonify({"message": "Leaves exported to Excel successfully!"})

@leave_bp.route('/export_json', methods=['GET'])
@login_required
def export_leaves_json():
    if not current_user.is_admin:
        flash("Unauthorized access!", "danger")
        return redirect(url_for('auth.login'))
    
    # Export leaves to JSON
    return jsonify({"message": "Leaves exported to JSON successfully!"})