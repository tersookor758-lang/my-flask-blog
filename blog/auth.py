from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user,
)

from models import db, User
from forms import RegisterForm, LoginForm

auth = Blueprint("auth", __name__)


# ---------------- REGISTER ----------------

@auth.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegisterForm()

    if form.validate_on_submit():

        username_exists = User.query.filter_by(
            username=form.username.data
        ).first()

        if username_exists:
            flash("Username already exists!", "danger")
            return redirect(url_for("auth.register"))

        email_exists = User.query.filter_by(
            email=form.email.data
        ).first()

        if email_exists:
            flash("Email already exists!", "danger")
            return redirect(url_for("auth.register"))

        user = User(
            username=form.username.data,
            email=form.email.data,
            password=generate_password_hash(form.password.data)
        )

        db.session.add(user)
        db.session.commit()

        flash(
            "Account created successfully! Please login.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template(
        "register.html",
        form=form
    )


# ---------------- LOGIN ----------------

@auth.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(
            email=form.email.data
        ).first()

        if user and check_password_hash(
            user.password,
            form.password.data
        ):

            login_user(user)

            flash(
                f"Welcome back, {user.username}!",
                "success"
            )

            return redirect(url_for("main.home"))

        flash(
            "Invalid email or password.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form
    )


# ---------------- LOGOUT ----------------

@auth.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "info"
    )

    return redirect(url_for("auth.login"))