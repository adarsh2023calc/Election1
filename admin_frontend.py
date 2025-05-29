from flask import Flask, render_template_string, redirect
import json
from flask import Blueprint, render_template
from sqlalchemy.orm import Session
from db import SessionLocal, Vote
import dotenv

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
      </ul>
    </div>
  </div>
</nav>



</body>
</html>
"""

@admin_bp.route('/')
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
        .hero {
            background: linear-gradient(to right, #0d6efd, #6610f2);
            color: white;
            padding: 4rem 2rem;
            text-align: center;
            border-radius: 0 0 2rem 2rem;
        }
        .results-section {
            margin-top: 2rem;
        }
        footer {
            background-color: #f8f9fa;
            text-align: center;
            padding: 1rem;
            margin-top: 4rem;
            border-top: 1px solid #dee2e6;
        }
    </style>
</head>
<body>

    <!-- Hero Section -->
    <section class="hero">
        <h1 class="display-4 fw-bold">Live Election Results</h1>
        <p class="lead">Real-time updates from the voting system</p>
    </section>

    <!-- Results Section -->
    <div class="container results-section">
        <h3 class="mb-4">Candidate Votes</h3>

        {% if counts %}
        <div class="row">
            {% for name, count in counts.items() %}
            <div class="col-md-4 mb-4">
                <div class="card border-success shadow-sm">
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

    """, counts=counts)

