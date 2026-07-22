from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    TextAreaField,
    SelectField
)
from wtforms.validators import (
    DataRequired,
    Email,
    Length,
    Optional,
    URL
)


# ---------------- REGISTER ----------------

class RegisterForm(FlaskForm):

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=6)
        ]
    )

    submit = SubmitField("Register")


# ---------------- LOGIN ----------------

class LoginForm(FlaskForm):

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    password = PasswordField(
        "Password",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Login")


# ---------------- CREATE / EDIT POST ----------------

class PostForm(FlaskForm):

    title = StringField(
        "Title",
        validators=[
            DataRequired(),
            Length(max=200)
        ]
    )

    content = TextAreaField(
        "Content",
        validators=[
            DataRequired()
        ]
    )

    category = SelectField(
        "Category",
        coerce=int,
        validators=[
            DataRequired()
        ],
        choices=[]
    )

    image = FileField(
        "Upload Image",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "gif", "webp"],
                "Images only!"
            )
        ]
    )

    video = FileField(
        "Upload Video",
        validators=[
            FileAllowed(
                ["mp4", "mov", "avi", "mkv", "webm"],
                "Videos only!"
            )
        ]
    )

    submit = SubmitField("Publish Post")


# ---------------- COMMENT ----------------

class CommentForm(FlaskForm):

    content = TextAreaField(
        "Write a comment...",
        validators=[
            DataRequired(),
            Length(min=1, max=500)
        ]
    )

    submit = SubmitField("Post Comment")


# ---------------- PROFILE ----------------

class ProfileForm(FlaskForm):

    first_name = StringField(
        "First Name",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    last_name = StringField(
        "Last Name",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(min=3, max=100)
        ]
    )

    email = StringField(
        "Email",
        validators=[
            DataRequired(),
            Email()
        ]
    )

    bio = TextAreaField(
        "Bio",
        validators=[
            Optional(),
            Length(max=300)
        ]
    )

    location = StringField(
        "Location",
        validators=[
            Optional(),
            Length(max=100)
        ]
    )

    website = StringField(
        "Website",
        validators=[
            Optional(),
            URL(require_tld=False)
        ]
    )

    profile_picture = FileField(
        "Profile Picture",
        validators=[
            FileAllowed(
                ["jpg", "jpeg", "png", "gif", "webp"],
                "Images only!"
            )
        ]
    )

    submit = SubmitField("Save Changes")