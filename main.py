from flask import Flask
from admin_frontend import admin_bp
from client_frontend import client_bp

app = Flask(__name__)
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(client_bp, url_prefix="/client")
