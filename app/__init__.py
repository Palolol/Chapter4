from flask import Flask, redirect, url_for
from config import Config
from extensions import db, csrf

def create_app(config_class: type[Config] = Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    csrf.init_app(app)

    # Register blueprints
    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp)

    # Add this block so "/" goes to the Users list 
    @app.route("/")
    def home():
        return redirect(url_for("users.index"))
    
    # Create tables 
    with app.app_context():
        from app.models import User # noqa: F401
        db.create_all()

    return app