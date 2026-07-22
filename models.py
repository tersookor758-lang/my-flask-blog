from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()


# =====================================================
# CATEGORY MODEL
# =====================================================

class Category(db.Model):

    __tablename__ = "categories"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    posts = db.relationship(
        "Post",
        back_populates="category",
        lazy=True
    )

    def __repr__(self):
        return f"<Category {self.name}>"


# =====================================================
# USER MODEL
# =====================================================

class User(UserMixin, db.Model):

    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    username = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )

    password = db.Column(
        db.String(255),
        nullable=False
    )

    first_name = db.Column(
        db.String(100)
    )

    last_name = db.Column(
        db.String(100)
    )

    bio = db.Column(
        db.Text
    )

    location = db.Column(
        db.String(100)
    )

    website = db.Column(
        db.String(255)
    )

    profile_picture = db.Column(
        db.String(255),
        default="default.png"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    posts = db.relationship(
        "Post",
        backref="author",
        lazy=True,
        cascade="all, delete-orphan"
    )

    comments = db.relationship(
        "Comment",
        backref="author",
        lazy=True,
        cascade="all, delete-orphan"
    )

    post_likes = db.relationship(
        "PostLike",
        back_populates="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    comment_likes = db.relationship(
        "CommentLike",
        back_populates="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<User {self.username}>"


# =====================================================
# POST MODEL
# =====================================================

class Post(db.Model):

    __tablename__ = "posts"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(200),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    image = db.Column(
        db.String(255)
    )

    video = db.Column(
        db.String(255)
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.id"),
        nullable=True
    )

    category = db.relationship(
        "Category",
        back_populates="posts"
    )

    comments = db.relationship(
        "Comment",
        backref="post",
        lazy=True,
        cascade="all, delete-orphan"
    )

    likes = db.relationship(
        "PostLike",
        back_populates="post",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Post {self.title}>"
    