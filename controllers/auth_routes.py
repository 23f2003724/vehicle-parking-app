from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.model import db, User, Admin
from werkzeug.security import check_password_hash

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        admin = Admin.query.filter_by(username=username).first()
        if admin and check_password_hash(admin.password, password):
            session['admin_id'] = admin.id
            flash("Admin login successful!", "success")
            return redirect(url_for('admin_routes.admin_dashboard'))

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            flash("User login successful!", "success")
            return redirect(url_for('user_routes.user_dashboard'))

        flash("Invalid username or password!", "danger")
        return redirect(url_for('auth_routes.login'))

    return render_template('login.html')

@auth_routes.route('/logout')
def logout():
    session.clear()
    flash("Logged out successfully!", "success")
    return redirect(url_for('auth_routes.login'))
