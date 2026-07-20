from flask import Blueprint, redirect, url_for, request
from flask_login import login_required, current_user

from models import (
    db,
    Post,
    Comment,
    PostLike,
    CommentLike
)


likes = Blueprint(
    "likes",
    __name__
)


# ---------------- POST LIKE / UNLIKE ----------------

@likes.route(
    "/post/<int:post_id>/like",
    methods=["POST"]
)
@login_required
def like_post(post_id):

    post = Post.query.get_or_404(
        post_id
    )

    existing_like = PostLike.query.filter_by(
        user_id=current_user.id,
        post_id=post.id
    ).first()

    if existing_like:

        db.session.delete(
            existing_like
        )

    else:

        new_like = PostLike(
            user_id=current_user.id,
            post_id=post.id
        )

        db.session.add(
            new_like
        )

    db.session.commit()

    return redirect(
        request.referrer or url_for("main.home")
    )


# ---------------- COMMENT LIKE / UNLIKE ----------------

@likes.route(
    "/comment/<int:comment_id>/like",
    methods=["POST"]
)
@login_required
def like_comment(comment_id):

    comment = Comment.query.get_or_404(
        comment_id
    )

    existing_like = CommentLike.query.filter_by(
        user_id=current_user.id,
        comment_id=comment.id
    ).first()


    if existing_like:

        db.session.delete(
            existing_like
        )

    else:

        new_like = CommentLike(
            user_id=current_user.id,
            comment_id=comment.id
        )

        db.session.add(
            new_like
        )


    db.session.commit()


    return redirect(
        request.referrer or url_for("main.home")
    )