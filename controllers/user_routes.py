from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.model import db, User, ParkingLot, ParkingSpot, Reservation
from werkzeug.security import generate_password_hash
from datetime import datetime
from zoneinfo import ZoneInfo
from pytz import timezone

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        address = request.form['address']
        pincode = request.form['pincode']

        existing_user = User.query.filter(
            (User.username == username) | (User.email == email)
        ).first()

        if existing_user:
            flash("❌ Username or Email already exists!", "danger")
            return redirect(url_for('user_routes.register'))

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        new_user = User(
            username=username,
            email=email,
            password=hashed_password,
            address=address,
            pincode=pincode
        )
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth_routes.login'))
    return render_template('user_register.html')

@user_routes.route('/user_dashboard')
def user_dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth_routes.login'))

    user_id = session['user_id']

    reservations = Reservation.query.filter_by(user_id=user_id) \
        .order_by(Reservation.timestamp.desc()) \
        .limit(5).all()

    ist = timezone('Asia/Kolkata')
    for r in reservations:
        r.timestamp_ist = r.timestamp.replace(tzinfo=timezone('UTC')).astimezone(ist).strftime("%d-%m-%Y %I:%M %p")
        if r.end_time:
            duration = r.end_time - r.timestamp
        else:
            duration = datetime.utcnow() - r.timestamp
        hours = int(duration.total_seconds() // 3600)
        minutes = int((duration.total_seconds() % 3600) // 60)
        r.duration_str = f"{hours} hr {minutes} min"

    lots = ParkingLot.query.all()

    return render_template('user_dashboard.html', reservations=reservations, lots=lots)

@user_routes.route('/lots')
def view_lots():
    lots = ParkingLot.query.all()
    return render_template('view_lots.html', lots=lots)

@user_routes.route('/book_auto/<int:lot_id>', methods=['POST'])
def auto_book_spot(lot_id):
    if 'user_id' not in session:
        flash("Please log in to book a spot.", "danger")
        return redirect(url_for('auth_routes.login'))

    vehicle_number = request.form.get('vehicle_number')
    if not vehicle_number:
        flash(" Vehicle number is required!", "danger")
        return redirect(url_for('user_routes.user_dashboard'))

    spot = ParkingSpot.query.filter_by(lot_id=lot_id, is_available=True).first()
    if not spot:
        flash(" No available spots in this parking lot.", "warning")
        return redirect(url_for('user_routes.user_dashboard'))
    
    reservation = Reservation(
        user_id=session['user_id'],
        spot_id=spot.id,
        vehicle_number=vehicle_number,
        start_time=datetime.now(ZoneInfo("Asia/Kolkata"))
    )
    spot.is_available = False

    db.session.add(reservation)
    db.session.commit()
    flash(f" Spot {spot.spot_number} booked successfully!", "success")
    return redirect(url_for('user_routes.reservation_history'))

@user_routes.route('/reservations')
def reservation_history():
    if 'user_id' not in session:
        return redirect(url_for('auth_routes.login'))

    user_id = session['user_id']
    reservations = Reservation.query.filter_by(user_id=user_id) \
        .order_by(Reservation.id.desc()).all()
    ist = timezone('Asia/Kolkata')  

    for r in reservations:
        r.timestamp_ist = r.timestamp.replace(tzinfo=timezone('UTC')).astimezone(ist).strftime("%d-%m-%Y %I:%M %p")
        if r.end_time:
            duration = r.end_time - r.timestamp
        else:
            duration = datetime.utcnow() - r.timestamp

        hours = int(duration.total_seconds() // 3600)
        minutes = int((duration.total_seconds() % 3600) // 60)
        r.duration_str = f"{hours} hr {minutes} min"

    return render_template('reservation_history.html', reservations=reservations)
         
@user_routes.route('/release_spot/<int:reservation_id>', methods=['GET', 'POST'])
def release_spot_form(reservation_id):
    if 'user_id' not in session:
        return redirect(url_for('auth_routes.login'))

    reservation = Reservation.query.get_or_404(reservation_id)
    spot = ParkingSpot.query.get(reservation.spot_id)

    if request.method == 'POST':
        spot.is_available = True
        db.session.delete(reservation)
        db.session.commit()
        flash(" Spot released successfully!", "success")
        return redirect(url_for('user_routes.reservation_history'))

    current_time = datetime.now(ZoneInfo("Asia/Kolkata"))

    if reservation.start_time.tzinfo is None:
        start_time_ist = reservation.start_time.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
    else:
        start_time_ist = reservation.start_time.astimezone(ZoneInfo("Asia/Kolkata"))

    duration = current_time - start_time_ist
    hours = int(duration.total_seconds() // 3600)
    minutes = int((duration.total_seconds() % 3600) // 60)
    total_hours = hours + 1 if minutes > 0 else hours
    hourly_rate = spot.lot.price_per_hour if spot and spot.lot else 0
    total_cost = total_hours * hourly_rate
    duration_str = f"{hours} hr {minutes} min"
    return render_template('release_spot.html',
                           reservation=reservation,
                           current_time=current_time.strftime("%Y-%m-%d %H:%M:%S"),
                           start_time=start_time_ist.strftime("%Y-%m-%d %H:%M:%S"),
                           duration_str=duration_str,
                           total_cost=total_cost)

@user_routes.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if 'user_id' not in session:
        return redirect(url_for('auth_routes.login'))
    user = User.query.get_or_404(session['user_id'])
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.address = request.form['address']
        user.pincode = request.form['pincode']

        db.session.commit()
        flash("Profile updated successfully!", "success")
        return redirect(url_for('user_routes.user_dashboard'))
    return render_template('edit_profile.html', user=user)


