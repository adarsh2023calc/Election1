from flask import Flask, render_template_string, redirect
import json
from flask import Blueprint, render_template
from sqlalchemy.orm import Session
from db import SessionLocal, Vote
import dotenv

from flask_login import LoginManager
from db import SessionLocal, User
from flask import request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash




admin_bp = Blueprint('admin', __name__)






dotenv.load_dotenv(".env.local")

base_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Election Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color: #f8f9fa; }
        .navbar { background-color: #003366; }
        .navbar-brand, .nav-link, .nav-link:hover { color: white !important; }
        .card { margin-top: 20px; }
    </style>
</head>
<body>


<nav class="navbar navbar-expand-lg navbar-dark">

  <div class="container-fluid">
    <a class="navbar-brand" href="/">Election Commission Dashboard</a>
    <div>
      <ul class="navbar-nav ms-auto">
        <li class="nav-item"><a class="nav-link" href="/">Home</a></li>
        <li class="nav-item"><a class="nav-link" href="/results">Results</a></li>
        {% if current_user.is_authenticated %}
            <li class="nav-item"><a class="nav-link" href="/admin/logout">Logout</a></li>
            {% else %}
            <li class="nav-item"><a class="nav-link" href="/admin/login">Login</a></li>
            {% endif %}
      </ul>
    </div>
  </div>
</nav>



</body>
</html>
"""

@admin_bp.route('/login', methods=['GET', 'POST'])

def login():
    if request.method == 'POST':
        db = SessionLocal()
        email = request.form.get('email')
        password = request.form.get('password')
        user = db.query(User).filter(User.email == email).first()
        db.close()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Invalid email or password', 'danger')

    return render_template_string(base_template + """
    <div class="container mt-5">
        <h2 class="text-center">Admin Login</h2>
        <form method="POST">
            <div class="mb-3">
                <label for="email" class="form-label">Email address</label>
                <input type="email" class="form-control" id="email" name="email" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
            <p class="mt-3">Don't have an account? <a href="{{ url_for('admin.register') }}">Register here</a></p>                  
        </form>
                                
    </div>
    """)

@admin_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        db = SessionLocal()
        email = request.form.get('email')
        password = request.form.get('password')
        
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            flash("Email already registered", "warning")
            db.close()
            return redirect(url_for('admin.register'))

        new_user = User(email=email, password=generate_password_hash(password))
        db.add(new_user)
        db.commit()
        db.close()

        flash("Registration successful. Please log in.", "success")
        return redirect(url_for('admin.login'))

    return render_template_string(base_template + """
    <div class="container mt-5">
        <h2 class="text-center">Register</h2>
        <form method="POST">
            <div class="mb-3">
                <label for="email" class="form-label">Email address</label>
                <input type="email" class="form-control" id="email" name="email" required>
            </div>
            <div class="mb-3">
                <label for="password" class="form-label">Password</label>
                <input type="password" class="form-control" id="password" name="password" required>
            </div>
            <button type="submit" class="btn btn-success">Register</button>
            <p class="mt-3">Already have an account? <a href="{{ url_for('admin.login') }}">Log here</a></p>  
        </form>
    </div>
    """)



@admin_bp.route('/')
@login_required
def dashboard():
    return render_template_string(base_template + """
    {% block content %}
    <div class="card">
        <div class="card-body text-center">
            <h3 class="card-title">Welcome to the Admin Dashboard</h3>
            <p class="card-text">Monitor and manage election results from here.</p>
            <a href="/admin/results" class="btn btn-primary">View Results</a>
            <a href="/client" class="btn btn-primary">Vote</a>
        </div>
    </div>
    {% endblock %}
    """)

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.login'))



@login_required
@admin_bp.route('/results')

def results():
    db: Session = SessionLocal()
    try:
        votes = db.query(Vote).all()
        counts = {}
        for vote in votes:
            candidate = vote.candidate
            counts[candidate] = counts.get(candidate, 0) + 1
        
    finally:
        db.close()


    return render_template_string(base_template + """
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Election Results</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f4f6f9;
            font-family: 'Segoe UI', sans-serif;
        }

        .hero {
            background: linear-gradient(135deg, #0d6efd, #6610f2);
            color: white;
            padding: 5rem 2rem;
            text-align: center;
            border-radius: 0 0 2rem 2rem;
            box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        }

        .hero h1 {
            font-size: 3.5rem;
        }

        .results-section {
            margin-top: 3rem;
        }

        .card {
            transition: transform 0.3s ease, box-shadow 0.3s ease;
            border: none;
            border-left: 5px solid #198754;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
        }

        .card-title {
            color: #0d6efd;
        }

        .alert {
            font-size: 1.2rem;
        }

        .btn-secondary {
            padding: 0.6rem 1.2rem;
            font-weight: 500;
            border-radius: 0.5rem;
        }

        footer {
            background-color: #ffffff;
            text-align: center;
            padding: 1.5rem 0;
            margin-top: 5rem;
            border-top: 1px solid #dee2e6;
            font-size: 0.95rem;
            color: #6c757d;
        }

        footer::before {
            content: "🗳️ ";
        }
    </style>
</head>
<body>

    <!-- Hero Section -->
    <section class="hero">
        <h1 class="fw-bold">Live Election Results</h1>
        <p class="lead">Real-time updates from the voting system</p>
    </section>

    <!-- Results Section -->
    <div class="container results-section">
        <h3 class="mb-4 text-center">Candidate Votes</h3>

        {% if counts %}
        <div class="row">
            {% for name, count in counts.items() %}
            <div class="col-md-4 mb-4">
                <div class="card shadow-sm">
                    <div class="card-body">
                        <h5 class="card-title">{{ name }}</h5>
                        <p class="card-text"><strong>Votes:</strong> {{ count }}</p>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        {% else %}
            <div class="alert alert-warning text-center" role="alert">
                No votes recorded yet.
            </div>
        {% endif %}

        <div class="text-center">
            <a href="/admin" class="btn btn-secondary mt-4">Back to Dashboard</a>
        </div>
    </div>

    <!-- Footer -->
    <footer>
        <p>&copy; {{ 2025 }} SecureVote | Built with Flask & Bootstrap</p>
    </footer>

</body>
</html>

</html>

    """, counts=counts)

