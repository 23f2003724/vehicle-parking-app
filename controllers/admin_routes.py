from flask import Blueprint, render_template, request, redirect, session, url_for, flash
from werkzeug.utils import secure_filename
import os
from sqlalchemy import case
from werkzeug.security import generate_password_hash
from models.model import db, Admin, User, ParkingLot, ParkingSpot, Reservation

admin_routes = Blueprint('admin_routes', __name__, url_prefix='/admin')

@admin_routes.route('/admin/dashboard')
def admin_dashboard():
    if 'admin_id' not in session:
        return redirect(url_for('auth_routes.login'))

    lots = ParkingLot.query.all()
    for lot in lots:
        lot.spots = ParkingSpot.query.filter_by(lot_id=lot.id).all()
        lot.occupied_spots = ParkingSpot.query.filter_by(lot_id=lot.id, is_available=False).count()
    return render_template('admin_dashboard.html', lots=lots)

@admin_routes.route('/admin/profile', methods=['GET', 'POST'])
def admin_profile():
    if 'admin_id' not in session:
        return redirect(url_for('auth_routes.login'))

    admin = Admin.query.get(session['admin_id'])

    if request.method == 'POST':
        admin.username = request.form['username']
        password = request.form.get('password')

        if password:
            admin.password = generate_password_hash(password, method='pbkdf2:sha256')

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('admin_routes.admin_profile'))

    return render_template('admin_profile.html', admin=admin)

@admin_routes.route('/admin/users')
def users():
    if 'admin_id' not in session:
        return redirect(url_for('auth_routes.login'))

    users = User.query.all()
    return render_template('users.html', users=users)

@admin_routes.route('/add-parkinglot', methods=['GET', 'POST'])
def add_parkinglot():
    if 'admin_id' not in session:
        return redirect(url_for('auth_routes.login'))

    if request.method == 'POST':
        prime_location_name = request.form['prime_location_name']
        address = request.form['address']
        pin_code = request.form['pin_code']
        price_per_hour = request.form['price_per_hour']
        max_spots = request.form['max_spots']

        image = request.files.get('image')
        filename = None

        if image and image.filename != '':
            filename = secure_filename(image.filename)
            upload_path = os.path.join('static/uploads', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            image.save(upload_path)

        lot = ParkingLot(
            prime_location_name=prime_location_name,
            address=address,
            pin_code=pin_code,
            price_per_hour=price_per_hour,
            max_spots=max_spots,
            image=filename
        )
        db.session.add(lot)
        db.session.commit()

        flash("Parking Lot added successfully!", "success")
        return redirect(url_for('admin_routes.admin_dashboard'))
    return render_template('add_parkinglot.html')

@admin_routes.route('/admin/parkinglot/<int:lot_id>/edit', methods=['GET', 'POST'])
def edit_parkinglot(lot_id):
    if 'admin_id' not in session:
        return redirect(url_for('auth_routes.login'))

    lot = ParkingLot.query.get_or_404(lot_id)

    if request.method == 'POST':
        lot.prime_location_name = request.form['prime_location_name']
        lot.address = request.form['address']
        lot.pin_code = request.form['pin_code']
        lot.price_per_hour = float(request.form['price_per_hour'])
        lot.max_spots = int(request.form['max_spots'])

        image = request.files.get('image')
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            upload_path = os.path.join('static/uploads', filename)
            os.makedirs(os.path.dirname(upload_path), exist_ok=True)
            image.save(upload_path)
            lot.image = filename

        db.session.commit()
        return redirect(url_for('admin_routes.admin_dashboard', lot_id=lot.id))
    return render_template('edit_parkinglot.html', lot=lot)

@admin_routes.route('/admin/parkinglot/<int:lot_id>/delete', methods=['POST'])
def delete_parkinglot(lot_id):
    if 'admin_id' not in session:
        return redirect(url_for('auth_routes.login'))

    lot = ParkingLot.query.get_or_404(lot_id)
    db.session.delete(lot)
    db.session.commit()
    flash(' Parking lot deleted successfully!', 'success')
    return redirect(url_for('admin_routes.admin_dashboard'))

@admin_routes.route('/admin/parkinglot/<int:lot_id>/spots', methods=['GET', 'POST'])
def manage_spots(lot_id):
    if 'admin_id' not in session:
        return redirect(url_for('auth_routes.login'))

    lot = ParkingLot.query.get_or_404(lot_id)

    if request.method == 'POST':
        if 'bulk_add' in request.form:
            prefix = request.form['prefix']
            count = int(request.form['count'])

            for i in range(1, count + 1):
                spot_number = f"{prefix}{i}"
                new_spot = ParkingSpot(spot_number=spot_number, lot_id=lot.id)
                db.session.add(new_spot)

            db.session.commit()
            flash(f'{count} spots added successfully!', 'success')

        else:
            spot_number = request.form['spot_number']
            new_spot = ParkingSpot(spot_number=spot_number, lot_id=lot.id)
            db.session.add(new_spot)
            db.session.commit()
            flash('Spot added successfully!', 'success')

    return render_template('manage_spots.html', lot=lot)

@admin_routes.route('/admin/parkinglot/<int:lot_id>/spot/<int:spot_id>/edit', methods=['GET', 'POST'])
def edit_spot(lot_id, spot_id):
    if 'admin_id' not in session:
        return redirect(url_for('auth_routes.login'))

    spot = ParkingSpot.query.get_or_404(spot_id)
    lot = ParkingLot.query.get_or_404(lot_id)

    if request.method == 'POST':
        spot.spot_number = request.form['spot_number']
        spot.is_available = True if request.form.get('is_available') == 'on' else False

        db.session.commit()
        flash('Spot updated successfully!', 'success')
        return redirect(url_for('admin_routes.manage_spots', lot_id=lot_id))
    return render_template('edit_spot.html', spot=spot, lot=lot)

@admin_routes.route('/admin/parkinglot/<int:lot_id>/spot/<int:spot_id>/delete', methods=['POST'])
def delete_spot(lot_id, spot_id):
    if 'admin_id' not in session:
        return redirect(url_for('auth_routes.login'))

    spot = ParkingSpot.query.get_or_404(spot_id)

    reservations = Reservation.query.filter_by(spot_id=spot.id).all()
    if reservations:
        flash("Cannot delete this spot. It has existing reservations.", "danger")
        return redirect(url_for("admin_routes.manage_spots", lot_id=lot_id))

    db.session.delete(spot)
    db.session.commit()
    flash('Spot deleted successfully!', 'success')
    return redirect(url_for('admin_routes.manage_spots', lot_id=lot_id))

@admin_routes.route('/summary')
def summary():
    if 'admin_id' not in session:
        return redirect(url_for('auth_routes.login'))

    total_users = User.query.count()
    total_lots = ParkingLot.query.count()
    total_spots = ParkingSpot.query.count()
    total_reservations = Reservation.query.count()

    return render_template('summary.html', 
                           total_users=total_users,
                           total_lots=total_lots,
                           total_spots=total_spots,
                           total_reservations=total_reservations)

@admin_routes.route('/admin/user-bookings')
def user_bookings():
    if 'admin_id' not in session:
        return redirect(url_for('auth_routes.login'))

    bookings = db.session.query(Reservation).join(User).join(ParkingSpot).join(ParkingLot).add_columns(
        Reservation.id,
        Reservation.vehicle_number,
        (Reservation.end_time == None).label('is_active'), 
        User.username.label('user_name'),
        User.email.label('user_email'),
        ParkingSpot.spot_number.label('spot_number'),
        ParkingLot.address.label('address')
    ).all()
    return render_template('user_bookings.html', bookings=bookings)
