import os

from flask import Flask, render_template
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash

from controllers.admin_routes import admin_routes
from controllers.auth_routes import auth_routes
from controllers.user_routes import user_routes
from models.model import Admin, db


def create_app():
    app = Flask(__name__)

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config["UPLOAD_FOLDER"] = os.path.join(basedir, "static/uploads")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///" + os.path.join(basedir, "parking.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-me")

    db.init_app(app)
    Migrate(app, db)

    app.register_blueprint(user_routes, url_prefix="/user")
    app.register_blueprint(admin_routes, url_prefix="/admin")
    app.register_blueprint(auth_routes)

    @app.route("/")
    def home():
        return render_template("home.html")

    return app


def seed_default_admin():
    admin_username = os.environ.get("ADMIN_USERNAME", "admin")
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")

    if not Admin.query.filter_by(username=admin_username).first():
        hashed_password = generate_password_hash(admin_password, method="pbkdf2:sha256")
        db.session.add(Admin(username=admin_username, password=hashed_password))
        db.session.commit()
        print(
            f"Default admin created: username={admin_username}. "
            "Set ADMIN_USERNAME and ADMIN_PASSWORD to override local dev credentials."
        )


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
        print("Database and tables created.")
        seed_default_admin()
    app.run(debug=True)
