"""empty message

Revision ID: f4f097120ddd
Revises: 8415e751adbf
Create Date: 2024-08-25 17:40:29.893015

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "f4f097120ddd"
down_revision = "8415e751adbf"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("users")
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "users",
        sa.Column("id", sa.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("age", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("first_name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("last_name", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("username", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("email", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("password", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="users_pkey"),
    )
    # ### end Alembic commands ###
