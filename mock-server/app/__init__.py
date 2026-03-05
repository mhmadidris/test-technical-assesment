from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from flask_cors import CORS
from config import Config
import os

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    CORS(app)

    # Automatically create tables if using SQLite
    if app.config['SQLALCHEMY_DATABASE_URI'].startswith('sqlite'):
        with app.app_context():
            db.create_all()

    # Register blueprints
    from app.routes.main import main_bp
    from app.routes.customers import customers_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(customers_bp, url_prefix='/api/customers')

    # Optional: data_bp if you still need it
    try:
        from app.routes.data import data_bp
        app.register_blueprint(data_bp, url_prefix='/api/v1/data')
    except ImportError:
        pass

    return app
