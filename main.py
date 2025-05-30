from flask import Flask
from admin_frontend import admin_bp
from client_frontend import client_bp


from flask import Flask
from flask_login import LoginManager
from db import SessionLocal, User


app = Flask(__name__)
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(client_bp, url_prefix="/client")
app.secret_key = "a_very_secret_key_123456" 
login_manager = LoginManager()
login_manager.login_view = 'admin.register'
login_manager.init_app(app)



@login_manager.user_loader
def load_user(user_id):
    db = SessionLocal()
    user = db.query(User).get(int(user_id))
    db.close()
    return user

