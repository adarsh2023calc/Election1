from flask import Flask, render_template_string, redirect
import json
from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__)

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
        </div>
    </div>
    {% endblock %}
    """)

@admin_bp.route('/results')
def results():
    try:
        with open('vote_store.json') as f:
            votes = json.load(f)
    except FileNotFoundError:
        votes = {}

    counts = {}
    for candidate in votes.values():
        counts[candidate] = counts.get(candidate, 0) + 1

    return render_template_string(base_template + """
    {% block content %}
    <h3 class="mb-3">Election Results</h3>
    {% if counts %}
    <div class="row">
        {% for name, count in counts.items() %}
        <div class="col-md-4">
            <div class="card border-success">
                <div class="card-body">
                    <h5 class="card-title">{{ name }}</h5>
                    <p class="card-text"><strong>Votes:</strong> {{ count }}</p>
                </div>
            </div>
        </div>
        {% endfor %}
    </div>
    {% else %}
        <p>No votes recorded yet.</p>
    {% endif %}
    <a href="/admin" class="btn btn-secondary mt-3">Back to Dashboard</a>
    {% endblock %}
    """, counts=counts)

