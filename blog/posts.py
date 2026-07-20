import os
import uuid

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    abort,
    request,
    current_app
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import secure_filename

from models import db, Post, Comment
from forms import PostForm, CommentForm


posts = Blueprint("posts", __name__)


@posts.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():

    form = PostForm()

    if form.validate_on_submit():

        image_filename = None
        video_filename = None

        if form.image.data:

            image = form.image.data

            image_filename = (
                f"{uuid.uuid4()}_"
                f"{secure_filename(image.filename)}"
            )

            image.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    image_filename
                )
            )

        if form.video.data:

            video = form.video.data

            video_filename = (
                f"{uuid.uuid4()}_"
                f"{secure_filename(video.filename)}"
            )

            video.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    video_filename
                )
            )

        post = Post(
            title=form.title.data,
            content=form.content.data,
            image=image_filename,
            video=video_filename,
            author=current_user
        )

        db.session.add(post)
        db.session.commit()

        flash(
            "Post created successfully!",
            "success"
        )

        return redirect(
            url_for("main.home")
        )

    return render_template(
        "create_post.html",
        form=form
    )


@posts.route(
    "/post/<int:post_id>",
    methods=["GET", "POST"]
)
def view_post(post_id):

    post = Post.query.get_or_404(post_id)

    form = CommentForm()

    if form.validate_on_submit():

        if not current_user.is_authenticated:
            abort(401)

        comment = Comment(
            content=form.content.data,
            post=post,
            author=current_user,
            parent_id=request.form.get("parent_id")
        )

        db.session.add(comment)
        db.session.commit()

        flash(
            "Comment added!",
            "success"
        )

        return redirect(
            url_for(
                "posts.view_post",
                post_id=post.id
            )
        )

    return render_template(
        "post.html",
        post=post,
        form=form
    )


@posts.route(
    "/post/<int:post_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = PostForm(obj=post)

    if form.validate_on_submit():

        post.title = form.title.data
        post.content = form.content.data

        if form.image.data:

            if post.image:

                old_image = os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    post.image
                )

                if os.path.exists(old_image):
                    os.remove(old_image)

            image = form.image.data

            image_filename = (
                f"{uuid.uuid4()}_"
                f"{secure_filename(image.filename)}"
            )

            image.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    image_filename
                )
            )

            post.image = image_filename

        if form.video.data:

            if post.video:

                old_video = os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    post.video
                )

                if os.path.exists(old_video):
                    os.remove(old_video)

            video = form.video.data

            video_filename = (
                f"{uuid.uuid4()}_"
                f"{secure_filename(video.filename)}"
            )

            video.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    video_filename
                )
            )

            post.video = video_filename

        db.session.commit()

        flash(
            "Post updated successfully!",
            "success"
        )

        return redirect(
            url_for(
                "posts.view_post",
                post_id=post.id
            )
        )

    return render_template(
        "edit_post.html",
        form=form,
        post=post
    )


@posts.route(
    "/post/<int:post_id>/delete",
    methods=["POST"]
)
@login_required
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    if post.image:

        image_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            post.image
        )

        if os.path.exists(image_path):
            os.remove(image_path)

    if post.video:

        video_path = os.path.join(
            current_app.config["UPLOAD_FOLDER"],
            post.video
        )

        if os.path.exists(video_path):
            os.remove(video_path)

    db.session.delete(post)

    db.session.commit()

    flash(
        "Post deleted successfully!",
        "success"
    )

    return redirect(
        url_for("main.home")
    )