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
        back_populates="author",
        cascade="all, delete-orphan",
        lazy=True
    )

    comments = db.relationship(
        "Comment",
        back_populates="author",
        cascade="all, delete-orphan",
        lazy=True
    )

    post_likes = db.relationship(
        "PostLike",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
    )

    comment_likes = db.relationship(
        "CommentLike",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy=True
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
        db.ForeignKey("categories.id")
    )

    author = db.relationship(
        "User",
        back_populates="posts"
    )

    category = db.relationship(
        "Category",
        back_populates="posts"
    )

    comments = db.relationship(
        "Comment",
        back_populates="post",
        cascade="all, delete-orphan",
        lazy=True
    )

    likes = db.relationship(
        "PostLike",
        back_populates="post",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Post {self.title}>"


# =====================================================
# COMMENT MODEL
# =====================================================

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
        db.ForeignKey("comments.id"),
        nullable=True
    )

    author = db.relationship(
        "User",
        back_populates="comments"
    )

    post = db.relationship(
        "Post",
        back_populates="comments"
    )

    replies = db.relationship(
        "Comment",
        backref=db.backref(
            "parent",
            remote_side=[id]
        ),
        cascade="all, delete-orphan",
        lazy=True
    )

    likes = db.relationship(
        "CommentLike",
        back_populates="comment",
        cascade="all, delete-orphan",
        lazy=True
    )

    def __repr__(self):
        return f"<Comment {self.id}>"


# =====================================================
# POST LIKE MODEL
# =====================================================

class PostLike(db.Model):

    __tablename__ = "post_likes"

    id = db.Column(
        db.Integer,
        primary_key=True
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

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "post_id",
            name="unique_post_like"
        ),
    )


# =====================================================
# COMMENT LIKE MODEL
# =====================================================

class CommentLike(db.Model):

    __tablename__ = "comment_likes"

    id = db.Column(
        db.Integer,
        primary_key=True
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

    __table_args__ = (
        db.UniqueConstraint(
            "user_id",
            "comment_id",
            name="unique_comment_like"
        ),
    )