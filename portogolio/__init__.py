from flask import Flask
import os
from models import storage
from flask_login import LoginManager
from models.user import User



app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("PORTOGOLIO_SECRET_KEY")
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'

@login_manager.user_loader
def load_user(user_id):
    return storage.get(User, user_id)


from portogolio import routes


