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

from models import (
    db,
    Post,
    Comment,
    Category
)

from forms import (
    PostForm,
    CommentForm
)

posts = Blueprint(
    "posts",
    __name__
)


# ==========================================================
# Upload Configuration
# ==========================================================

ALLOWED_IMAGE_EXTENSIONS = {
    "jpg",
    "jpeg",
    "png",
    "gif",
    "webp"
}

ALLOWED_VIDEO_EXTENSIONS = {
    "mp4",
    "mov",
    "avi",
    "mkv",
    "webm"
}

MAX_IMAGE_SIZE = 50 * 1024 * 1024          # 50 MB
MAX_VIDEO_SIZE = 1536 * 1024 * 1024        # 1.5 GB


# ==========================================================
# Helper Functions
# ==========================================================

def save_uploaded_file(file):

    if file is None:
        return None

    # Happens when editing a post and WTForms
    # passes the existing filename instead of a file.
    if isinstance(file, str):
        return None

    if not hasattr(file, "filename"):
        return None

    if file.filename == "":
        return None

    upload_folder = current_app.config["UPLOAD_FOLDER"]

    os.makedirs(
        upload_folder,
        exist_ok=True
    )

    filename = (
        f"{uuid.uuid4()}_"
        f"{secure_filename(file.filename)}"
    )

    file.save(
        os.path.join(
            upload_folder,
            filename
        )
    )

    return filename


def delete_uploaded_file(filename):

    if not filename:
        return

    path = os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )

    if os.path.exists(path):
        os.remove(path)


# ==========================================================
# CREATE POST
# ==========================================================

@posts.route(
    "/create-post",
    methods=["GET", "POST"]
)
@login_required
def create_post():

    form = PostForm()

    form.category.choices = [

        (category.id, category.name)

        for category in
        Category.query.order_by(
            Category.name
        ).all()

    ]

    if form.validate_on_submit():

        image_filename = save_uploaded_file(
            form.image.data
        )

        video_filename = save_uploaded_file(
            form.video.data
        )

        post = Post(

            title=form.title.data,

            content=form.content.data,

            image=image_filename,

            video=video_filename,

            author=current_user,

            category_id=form.category.data

        )

        db.session.add(post)

        db.session.commit()

        flash(
            "Post published successfully.",
            "success"
        )

        return redirect(
            url_for(
                "posts.view_post",
                post_id=post.id
            )
        )

    return render_template(
        "create_post.html",
        form=form
    )


# ==========================================================
# VIEW POST
# ==========================================================

@posts.route(
    "/post/<int:post_id>"
)
def view_post(post_id):

    post = Post.query.get_or_404(post_id)

    comment_form = CommentForm()

    comments = (
        Comment.query
        .filter_by(
            post_id=post.id,
            parent_id=None
        )
        .order_by(
            Comment.created_at.asc()
        )
        .all()
    )

    total_comments = Comment.query.filter_by(
        post_id=post.id
    ).count()

    total_post_likes = len(post.likes)

    return render_template(
        "view_post.html",
        post=post,
        comments=comments,
        comment_form=comment_form,
        total_comments=total_comments,
        total_post_likes=total_post_likes
    )
# ==========================================================
# EDIT POST
# ==========================================================

@posts.route(
    "/post/<int:post_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = PostForm()

    form.category.choices = [

        (category.id, category.name)

        for category in
        Category.query.order_by(
            Category.name
        ).all()

    ]

    if request.method == "GET":

        form.title.data = post.title

        form.content.data = post.content

        form.category.data = post.category_id

    if form.validate_on_submit():

        post.title = form.title.data

        post.content = form.content.data

        post.category_id = form.category.data

        new_image = save_uploaded_file(
            form.image.data
        )

        if new_image:

            delete_uploaded_file(
                post.image
            )

            post.image = new_image

        new_video = save_uploaded_file(
            form.video.data
        )

        if new_video:

            delete_uploaded_file(
                post.video
            )

            post.video = new_video

        db.session.commit()

        flash(
            "Post updated successfully.",
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


# ==========================================================
# DELETE POST
# ==========================================================

@posts.route(
    "/post/<int:post_id>/delete",
    methods=["POST"]
)
@login_required
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    delete_uploaded_file(
        post.image
    )

    delete_uploaded_file(
        post.video
    )

    db.session.delete(post)

    db.session.commit()

    flash(
        "Post deleted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "main.home"
        )
    )
# ==========================================================
# ADD COMMENT
# ==========================================================

@posts.route(
    "/post/<int:post_id>/comment",
    methods=["POST"]
)
@login_required
def add_comment(post_id):

    post = Post.query.get_or_404(post_id)

    form = CommentForm()

    if not form.validate_on_submit():

        flash(
            "Comment cannot be empty.",
            "danger"
        )

        return redirect(
            url_for(
                "posts.view_post",
                post_id=post.id
            )
        )

    comment = Comment(

        content=form.content.data,

        author=current_user,

        post=post

    )

    db.session.add(comment)

    db.session.commit()

    flash(
        "Comment added successfully.",
        "success"
    )

    return redirect(
        url_for(
            "posts.view_post",
            post_id=post.id
        )
    )


# ==========================================================
# REPLY TO COMMENT
# ==========================================================

@posts.route(
    "/comment/<int:comment_id>/reply",
    methods=["POST"]
)
@login_required
def reply_comment(comment_id):

    parent_comment = Comment.query.get_or_404(
        comment_id
    )

    form = CommentForm()

    if not form.validate_on_submit():

        flash(
            "Reply cannot be empty.",
            "danger"
        )

        return redirect(
            url_for(
                "posts.view_post",
                post_id=parent_comment.post_id
            )
        )

    reply = Comment(

        content=form.content.data,

        author=current_user,

        post_id=parent_comment.post_id,

        parent_id=parent_comment.id

    )

    db.session.add(reply)

    db.session.commit()

    flash(
        "Reply posted successfully.",
        "success"
    )

    return redirect(
        url_for(
            "posts.view_post",
            post_id=parent_comment.post_id
        )
    )


# ==========================================================
# REMOVE POST IMAGE
# ==========================================================

@posts.route(
    "/post/<int:post_id>/remove-image",
    methods=["POST"]
)
@login_required
def remove_post_image(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    delete_uploaded_file(
        post.image
    )

    post.image = None

    db.session.commit()

    flash(
        "Image removed successfully.",
        "success"
    )

    return redirect(
        url_for(
            "posts.edit_post",
            post_id=post.id
        )
    )


# ==========================================================
# REMOVE POST VIDEO
# ==========================================================

@posts.route(
    "/post/<int:post_id>/remove-video",
    methods=["POST"]
)
@login_required
def remove_post_video(post_id):

    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    delete_uploaded_file(
        post.video
    )

    post.video = None

    db.session.commit()

    flash(
        "Video removed successfully.",
        "success"
    )

    return redirect(
        url_for(
            "posts.edit_post",
            post_id=post.id
        )
    )