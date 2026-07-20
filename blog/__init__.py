import os

from flask import Flask
from flask_login import LoginManager

from models import db, User


login_manager = LoginManager()
login_manager.login_view = "auth.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


def create_app():

    app = Flask(
        __name__,
        template_folder="../templates"
    )

    # =====================================
    # Flask Configuration
    # =====================================

    app.config["SECRET_KEY"] = "your_secret_key"

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # =====================================
    # Upload Configuration
    # =====================================

    app.config["UPLOAD_FOLDER"] = os.path.join(
        app.root_path,
        "static",
        "uploads"
    )

    # Flask request size limit (~1.1 GB)
    #
    # This allows:
    # - Images up to 30 MB
    # - Videos up to 1 GB
    #
    # Individual file validation is handled
    # inside blog/posts.py.

    app.config["MAX_CONTENT_LENGTH"] = 1100 * 1024 * 1024

    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    # =====================================
    # Initialize Extensions
    # =====================================

    db.init_app(app)

    login_manager.init_app(app)

    # =====================================
    # Register Blueprints
    # =====================================

    from blog.routes import main
    app.register_blueprint(main)

    from blog.auth import auth
    app.register_blueprint(auth)

    from blog.posts import posts
    app.register_blueprint(posts)

    from blog.profile import profile
    app.register_blueprint(profile)

    from blog.likes import likes
    app.register_blueprint(likes)

    from blog.users import users
    app.register_blueprint(users)

    from blog.comments import comments
    app.register_blueprint(comments)

    # =====================================
    # Create Database Tables
    # =====================================

    with app.app_context():
        db.create_all()

    return app