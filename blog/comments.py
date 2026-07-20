from flask import (
    Blueprint,
    redirect,
    url_for,
    request,
    flash,
    abort
)

from flask_login import (
    login_required,
    current_user
)

from models import (
    db,
    Comment
)


comments = Blueprint(
    "comments",
    __name__
)


@comments.route(
    "/comment/<int:comment_id>/edit",
    methods=["POST"]
)
@login_required
def edit_comment(comment_id):

    comment = Comment.query.get_or_404(comment_id)

    if comment.user_id != current_user.id:
        abort(403)

    content = request.form.get("content", "").strip()

    if not content:

        flash(
            "Comment cannot be empty.",
            "danger"
        )

        return redirect(
            url_for(
                "posts.view_post",
                post_id=comment.post_id
            )
        )

    comment.content = content

    db.session.commit()

    flash(
        "Comment updated successfully.",
        "success"
    )

    return redirect(
        url_for(
            "posts.view_post",
            post_id=comment.post_id
        )
    )


@comments.route(
    "/comment/<int:comment_id>/delete",
    methods=["POST"]
)
@login_required
def delete_comment(comment_id):

    comment = Comment.query.get_or_404(comment_id)

    if comment.user_id != current_user.id:
        abort(403)

    post_id = comment.post_id

    db.session.delete(comment)

    db.session.commit()

    flash(
        "Comment deleted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "posts.view_post",
            post_id=post_id
        )
    )