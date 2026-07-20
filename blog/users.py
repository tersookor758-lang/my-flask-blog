from flask import Blueprint, render_template
from models import User


users = Blueprint(
    "users",
    __name__
)


@users.route("/users/<string:username>")
def user_profile(username):

    user = User.query.filter_by(
        username=username
    ).first_or_404()

    posts = sorted(
        user.posts,
        key=lambda post: post.created_at,
        reverse=True
    )

    return render_template(
        "user_profile.html",
        user=user,
        posts=posts
    )