from flask import Blueprint, render_template

downloads_bp = Blueprint('downloads', __name__)

@downloads_bp.route('/downloads')
def downloads():
    return render_template('downloads.html')
