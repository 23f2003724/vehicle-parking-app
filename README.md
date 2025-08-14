#  Vehicle Parking Management System - MAD-1 Project

## Overview

This project is a **Smart Parking Management System** developed using **Flask** as part of the *Modern Application Development - 1 (MAD-1)* course. It offers two separate dashboards for **Admins** and **Users**, supporting parking lot management, user authentication, and real-time spot reservation.

---

## Features

###  User Functionality

* Register, login, and logout
* View all available parking lots
* Automatically book the first available spot by entering vehicle number
* View their own reservation history

### Admin Functionality

* Secure admin login
* Add, edit, and delete parking lots
* Add, edit, and delete parking spots within lots
* View list of all registered users
* View all reservations made by users

---
## Technologies Used

- **Flask**: Backend web framework
- **SQLAlchemy & Flask-SQLAlchemy**: ORM for database management
- **SQLite**: Lightweight relational database engine
- **Bootstrap**: Responsive frontend design via CDN

---

##  Milestones Completed

-  GitHub Repository Setup  
-  Database Models and Schema Setup  
-  User Authentication System  
-  User Registration System  
-  User Authentication & Session Management  
-  Admin Dashboard & Management  
-  Parking Spot Reservation  
-  Release Parking Spot Functionality  

---

## Models

- **Admin:** Stores admin username and password for authentication.
- **User:** Contains user details like username, email, address, pincode, and password.
- **ParkingLot:** Represents a parking lot with a prime location name and address.
- **ParkingSpot:** Represents individual spots within a parking lot. Tracks spot number, availability, and associated lot.
- **Reservation:** Records reservations made by users, including user ID, spot ID, vehicle number, and timestamp.

---

## Project Structure

```
PARKING_APP_23F2003724/
├── app.py
├── parking.db
├── controllers/
│   ├── admin_routes.py
│   ├── auth_routes.py
│   └── user_routes.py
├── models/
│   └── model.py
├── templates/
│   ├── add_parkinglot.html
│   ├── admin_dashboard.html
│   ├── admin_profile.html
│   ├── edit_parkinglot.html
│   ├── edit_profile.html
│   ├── edit_spot.html
│   ├── home.html
│   ├── login.html
│   ├── manage_spots.html
│   ├── release_spot.html
│   ├── reservation_history.html
│   ├── summary.html
│   ├── user_bookings.html
│   ├── user_dashboard.html
│   ├── user_register.html
│   ├── users.html
│   ├── view_lots.html
│   └── view_spots.html
└── parking_app_23f2003724.code-workspace
```

---

##  Academic Note

This project was created solely for academic purposes as part of the **Modern Application Development - 1 (MAD-1)** curriculum under the **B.Sc. in Data Science and Applications, IIT Madras**.