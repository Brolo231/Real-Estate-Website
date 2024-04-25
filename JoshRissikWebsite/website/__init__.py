from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from website.utils import format_price

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['PERMANENT_SESSION_LIFETIME'] = 3600

    app.config['UPLOAD_FOLDER'] = 'website/static/property_images'
    app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

    app.jinja_env.filters['format_price'] = format_price

    db.init_app(app)

    from .views import user, admin
    app.register_blueprint(user)
    app.register_blueprint(admin)

    return app