# import os
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from .config import Config
# from flask_login import LoginManager, login_manager
# from flask_bcrypt import Bcrypt

# # App Setup
# app = Flask(__name__)
# app.config.from_object(Config)
# app.secret_key = os.urandom(24)  

# # DB Setup
# db = SQLAlchemy(app)

# # Auth
# # login_manager = LoginManager()
# # login_manager.login_view = "auth.login"
# # login_manager.init_app(app)


# # App Context
# with app.app_context():
#     db.create_all()