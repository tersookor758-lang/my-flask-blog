from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()


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


class Comment(db.Model):

    __tablename__ = "comments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    content = db.Column(
        db.Text,
        nullable=False
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

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        nullable=False
    )

    parent_id = db.Column(
        db.Integer,
        db.ForeignKey("comments.id")
    )

    replies = db.relationship(
        "Comment",
        backref=db.backref(
            "parent",
            remote_side=[id]
        ),
        lazy=True,
        cascade="all, delete-orphan"
    )

    likes = db.relationship(
        "CommentLike",
        back_populates="comment",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Comment {self.id}>"


class PostLike(db.Model):

    __tablename__ = "post_likes"

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "post_id",
            name="unique_post_like"
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True
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

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="post_likes"
    )

    post = db.relationship(
        "Post",
        back_populates="likes"
    )

    def __repr__(self):
        return f"<PostLike User={self.user_id} Post={self.post_id}>"


class CommentLike(db.Model):

    __tablename__ = "comment_likes"

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "comment_id",
            name="unique_comment_like"
        ),
    )

    id = db.Column(
        db.Integer,
        primary_key=True
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

    comment_id = db.Column(
        db.Integer,
        db.ForeignKey("comments.id"),
        nullable=False
    )

    user = db.relationship(
        "User",
        back_populates="comment_likes"
    )

    comment = db.relationship(
        "Comment",
        back_populates="likes"
    )

    def __repr__(self):
        return f"<CommentLike User={self.user_id} Comment={self.comment_id}>"