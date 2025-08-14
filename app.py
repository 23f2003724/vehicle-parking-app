from flask import Flask, render_template
from werkzeug.security import generate_password_hash
import os
from flask_migrate import Migrate
from models.model import db, Admin, User, ParkingLot, ParkingSpot, Reservation
from controllers.user_routes import user_routes
from controllers.admin_routes import admin_routes
from controllers.auth_routes import auth_routes

def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'static/uploads')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'parking.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'supersecretkey'

    db.init_app(app) 
    migrate = Migrate(app, db) 
    app.register_blueprint(user_routes, url_prefix='/user')
    app.register_blueprint(admin_routes, url_prefix='/admin')  
    app.register_blueprint(auth_routes)


    @app.route('/')
    def home():
        return render_template('home.html')
    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        print(" Database and tables created!")

        if not Admin.query.filter_by(username="admin").first():
            hashed_password = generate_password_hash("admin123", method='pbkdf2:sha256')
            new_admin = Admin(username="admin", password=hashed_password)
            db.session.add(new_admin)
            db.session.commit()
            print("Default admin created: username=admin, password=admin123")
    app.run(debug=True)
