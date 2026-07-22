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

    page = request.args.get(
        "page",
        1,
        type=int
    )

    query = (
        Post.query
        .join(User)
    )

    if search:

        query = query.filter(
            or_(
                Post.title.ilike(f"%{search}%"),
                Post.content.ilike(f"%{search}%"),
                User.username.ilike(f"%{search}%")
            )
        )

    posts = (
        query
        .order_by(
            Post.created_at.desc()
        )
        .paginate(
            page=page,
            per_page=5,
            error_out=False
        )
    )

    return render_template(
        "index.html",
        posts=posts,
        search=search
    )