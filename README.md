# Vehicle Parking Management System

A Flask-based parking management web application with separate admin and user workflows. The project demonstrates backend routing, database modeling, authentication, CRUD operations, and a responsive Bootstrap UI.

## Highlights

- Role-based login for admin and users
- User registration and session-based authentication
- Admin dashboard for parking lots, parking spots, users, and reservations
- Parking lot CRUD with price, location, image, and capacity fields
- Parking spot creation, editing, deletion, and availability tracking
- User dashboard for viewing lots, reserving spots, and checking booking history
- SQLite database for local development with Flask-SQLAlchemy models
- Flask-Migrate setup for schema migrations

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Migrate
- SQLite
- Jinja templates
- Bootstrap

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Open the app at `http://127.0.0.1:5000`.

For local development, the app creates the database tables automatically when you run `python app.py`.

## Local Admin Login

By default, the app creates a local development admin account if one does not already exist.

```text
Username: admin
Password: admin123
```

You can override these values before running the app:

```bash
set SECRET_KEY=your-secret-key
set ADMIN_USERNAME=admin
set ADMIN_PASSWORD=your-strong-password
python app.py
```

## Project Structure

```text
.
|-- app.py
|-- controllers/
|   |-- admin_routes.py
|   |-- auth_routes.py
|   `-- user_routes.py
|-- models/
|   `-- model.py
|-- templates/
|-- static/
|   `-- uploads/
|-- migrations/
|-- requirements.txt
|-- Procfile
`-- README.md
```

## What This Project Shows

This project is useful as a beginner Python backend portfolio project because it includes practical web-development concepts: route organization with blueprints, relational data models, password hashing, server-side sessions, CRUD screens, file uploads, and local deployment setup.

## Next Improvements

- Add automated tests for authentication and reservation flows
- Move local admin creation into a Flask CLI command
- Add form validation helpers to reduce repeated checks
- Add production deployment notes with environment variables

## Academic Context

Built as part of Modern Application Development coursework while learning practical Flask application development.
