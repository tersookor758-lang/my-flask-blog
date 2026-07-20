from flask import Blueprint, render_template
from models import Post

main = Blueprint("main", __name__)


@main.route("/")
def home():

    posts = Post.query.order_by(
        Post.created_at.desc()
    ).all()

    return render_template(
        "index.html",
        posts=posts
    )