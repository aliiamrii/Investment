from flask import Flask
<<<<<<< HEAD
from flask_jwt_extended import JWTManager
from app.config import config
from app.models import db
from app.auth import auth
from app.account import account
=======
from flask_jwt_extended import JWTManager # type: ignore
from app.config import config
from app.models import db
from app.auth import auth
from app.investment import investment
from app.admin import admin 
>>>>>>> 6873958458b7c396f826c02bb2bd911cc5fba600

def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

<<<<<<< HEAD
    try:
        db.init_app(app)
    except Exception as e:
        print(f"Error initializing database: {e}")
        return None

    jwt_manager = JWTManager(app)
    jwt_manager.secret_key = app.config['JWT_SECRET_KEY']
    jwt_manager.access_token_expires = app.config['JWT_ACCESS_TOKEN_EXPIRES']

    app.register_blueprint(auth, url_prefix='/api/v1/auth')
    app.register_blueprint(account, url_prefix='/api/v1/account')
=======
    db.init_app(app)
    JWTManager(app)

    app.register_blueprint(auth, url_prefix='/api/v1/auth')
    app.register_blueprint(investment, url_prefix='/api/v1/investments')  
    app.register_blueprint(admin, url_prefix='/api/v1/admin') 
>>>>>>> 6873958458b7c396f826c02bb2bd911cc5fba600

    return app
