"""Add follow system

Revision ID: 3924bd02cbde
Revises: 2634fc27d4b5
Create Date: 2026-07-31 10:09:08.013546

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3924bd02cbde"
down_revision = "2634fc27d4b5"
branch_labels = None
depends_on = None


def upgrade():

    op.create_table(
        "follows",

        sa.Column(
            "id",
            sa.Integer(),
            primary_key=True
        ),

        sa.Column(
            "follower_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "following_id",
            sa.Integer(),
            nullable=False
        ),

        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=True
        ),

        sa.ForeignKeyConstraint(
            ["follower_id"],
            ["users.id"],
            name="fk_follows_follower"
        ),

        sa.ForeignKeyConstraint(
            ["following_id"],
            ["users.id"],
            name="fk_follows_following"
        ),

        sa.UniqueConstraint(
            "follower_id",
            "following_id",
            name="unique_follow"
        )
    )


def downgrade():

    op.drop_table(
        "follows"
    )