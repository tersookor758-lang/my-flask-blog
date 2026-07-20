import os
import uuid

from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    current_app,
    abort
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.utils import secure_filename

from models import (
    db,
    User
)

from forms import ProfileForm


profile = Blueprint(
    "profile",
    __name__
)


# ---------------------------------------
# MY PROFILE
# ---------------------------------------

@profile.route("/profile")
@login_required
def view_profile():

    return render_template(
        "profile.html",
        user=current_user
    )


# ---------------------------------------
# PUBLIC USER PROFILE
# ---------------------------------------

@profile.route("/user/<string:username>")
def user_profile(username):

    user = User.query.filter_by(
        username=username
    ).first_or_404()

    return render_template(
        "user_profile.html",
        user=user
    )


# ---------------------------------------
# EDIT PROFILE
# ---------------------------------------

@profile.route(
    "/profile/edit",
    methods=["GET", "POST"]
)
@login_required
def edit_profile():

    form = ProfileForm()

    if form.validate_on_submit():

        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        current_user.location = form.location.data
        current_user.website = form.website.data

        if form.profile_picture.data:

            if (
                current_user.profile_picture
                and current_user.profile_picture != "default.png"
            ):

                old_picture = os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    current_user.profile_picture
                )

                if os.path.exists(old_picture):
                    os.remove(old_picture)

            picture = form.profile_picture.data

            filename = (
                f"{uuid.uuid4()}_"
                f"{secure_filename(picture.filename)}"
            )

            picture.save(
                os.path.join(
                    current_app.config["UPLOAD_FOLDER"],
                    filename
                )
            )

            current_user.profile_picture = filename

        db.session.commit()

        flash(
            "Profile updated successfully!",
            "success"
        )

        return redirect(
            url_for("profile.view_profile")
        )

    if not form.is_submitted():

        form.first_name.data = current_user.first_name
        form.last_name.data = current_user.last_name
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.location.data = current_user.location
        form.website.data = current_user.website

    return render_template(
        "profile.html",
        form=form,
        user=current_user,
        edit_mode=True
    )