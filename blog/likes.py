from flask import (
    Blueprint,
    redirect,
    url_for,
    request,
    flash
)

from flask_login import (
    login_required,
    current_user
)

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



# ==================================================
# POST LIKE / UNLIKE
# ==================================================

@likes.route(
    "/post/<int:post_id>/like",
    methods=["POST"]
)
@login_required
def like_post(post_id):

    post = db.session.get(
        Post,
        post_id
    )

    if not post:
        flash(
            "Post not found.",
            "danger"
        )

        return redirect(
            request.referrer or url_for("main.home")
        )


    existing_like = PostLike.query.filter_by(
        user_id=current_user.id,
        post_id=post.id
    ).first()



    if existing_like:

        db.session.delete(
            existing_like
        )

        flash(
            "Post unliked.",
            "info"
        )


    else:

        new_like = PostLike(
            user_id=current_user.id,
            post_id=post.id
        )

        db.session.add(
            new_like
        )

        flash(
            "Post liked.",
            "success"
        )



    db.session.commit()



    return redirect(
        request.referrer or url_for("main.home")
    )





# ==================================================
# COMMENT LIKE / UNLIKE
# ==================================================

@likes.route(
    "/comment/<int:comment_id>/like",
    methods=["POST"]
)
@login_required
def like_comment(comment_id):

    comment = db.session.get(
        Comment,
        comment_id
    )


    if not comment:

        flash(
            "Comment not found.",
            "danger"
        )

        return redirect(
            request.referrer or url_for("main.home")
        )



    existing_like = CommentLike.query.filter_by(
        user_id=current_user.id,
        comment_id=comment.id
    ).first()



    if existing_like:

        db.session.delete(
            existing_like
        )

        flash(
            "Comment unliked.",
            "info"
        )


    else:

        new_like = CommentLike(
            user_id=current_user.id,
            comment_id=comment.id
        )

        db.session.add(
            new_like
        )

        flash(
            "Comment liked.",
            "success"
        )



    db.session.commit()



    return redirect(
        request.referrer or url_for("main.home")
    )