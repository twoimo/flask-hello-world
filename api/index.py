from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from routes import main, auth, inquiry
from models.user import User

db = SQLAlchemy()
login_manager = LoginManager()

app = Flask(__name__)
app.config.from_object(Config)

app.register_blueprint(main.main)
app.register_blueprint(auth.auth)
app.register_blueprint(inquiry.inquiry)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()