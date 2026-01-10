# from flask import Flask
# from .config import Config
# from .extensions import db, login_manager

# def create_app():
#     app = Flask(__name__, template_folder="templates", static_folder="static")
#     app.config.from_object(Config)

#     db.init_app(app)
#     login_manager.init_app(app)

#     # Import and register blueprints
#     from .auth.routes import auth_bp
#     from .admin.routes import admin_bp
#     from .shop.routes import shop_bp

#     app.register_blueprint(auth_bp)
#     app.register_blueprint(admin_bp)
#     app.register_blueprint(shop_bp)

#     with app.app_context():
#         db.create_all()

#     return app


import os
from flask import Flask
from .extensions import db, login_manager
from .admin.routes import admin_bp
from .shop.routes import shop_bp
from .auth.routes import auth_bp

def create_app():
    app = Flask(__name__)

    # Load config
    app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "change-me")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///mini_shop.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = os.environ.get("UPLOAD_FOLDER", os.path.join(app.root_path, 'static/uploads'))
    app.config['ALLOWED_EXTENSIONS'] = set(os.environ.get("ALLOWED_EXTENSIONS", "png,jpg,jpeg,gif").split(","))

    # Ensure upload folder exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)

    # Register blueprints
    app.register_blueprint(admin_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(auth_bp)

    # Create tables
    with app.app_context():
        db.create_all()

    return app
