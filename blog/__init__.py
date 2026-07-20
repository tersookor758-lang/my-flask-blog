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

    app.config["SECRET_KEY"] = "your_secret_key"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["UPLOAD_FOLDER"] = os.path.join(
        app.root_path,
        "static",
        "uploads"
    )

    app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024

    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    db.init_app(app)
    login_manager.init_app(app)

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

    with app.app_context():
        db.create_all()

    return app