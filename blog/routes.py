from flask import (
    Blueprint,
    render_template,
    request
)

from sqlalchemy import or_

from models import Post, User


main = Blueprint(
    "main",
    __name__
)


@main.route("/")
def home():

    search = request.args.get(
        "search",
        ""
    ).strip()

    if search:

        posts = (
            Post.query
            .join(User)
            .filter(
                or_(
                    Post.title.ilike(f"%{search}%"),
                    Post.content.ilike(f"%{search}%"),
                    User.username.ilike(f"%{search}%")
                )
            )
            .order_by(
                Post.created_at.desc()
            )
            .all()
        )

    else:

        posts = (
            Post.query
            .order_by(
                Post.created_at.desc()
            )
            .all()
        )

    return render_template(
        "index.html",
        posts=posts,
        search=search
    )