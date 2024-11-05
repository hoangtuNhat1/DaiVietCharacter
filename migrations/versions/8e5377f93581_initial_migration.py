"""Initial migration

Revision ID: 8e5377f93581
Revises: 
Create Date: 2024-11-05 21:05:00.533566

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = "8e5377f93581"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "characters",
        "created_at",
        existing_type=mysql.TIMESTAMP(),
        nullable=False,
        existing_server_default=sa.text("(now())"),
    )
    op.alter_column(
        "characters",
        "updated_at",
        existing_type=mysql.TIMESTAMP(),
        nullable=False,
        existing_server_default=sa.text("(now())"),
    )
    op.drop_index("ix_characters_id", table_name="characters")
    op.add_column(
        "user_accounts", sa.Column("role", sa.String(length=50), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user_accounts", "role")
    op.create_index("ix_characters_id", "characters", ["id"], unique=False)
    op.alter_column(
        "characters",
        "updated_at",
        existing_type=mysql.TIMESTAMP(),
        nullable=True,
        existing_server_default=sa.text("(now())"),
    )
    op.alter_column(
        "characters",
        "created_at",
        existing_type=mysql.TIMESTAMP(),
        nullable=True,
        existing_server_default=sa.text("(now())"),
    )
    op.create_table(
        "history_logs",
        sa.Column("id", mysql.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("user_id", mysql.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("agent_id", mysql.INTEGER(), autoincrement=False, nullable=True),
        sa.Column("question", mysql.TEXT(), nullable=False),
        sa.Column("prompt", mysql.TEXT(), nullable=False),
        sa.Column("answer", mysql.TEXT(), nullable=False),
        sa.Column("feedback", mysql.ENUM("like", "dislike"), nullable=True),
        sa.Column(
            "created_at",
            mysql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.ForeignKeyConstraint(
            ["agent_id"], ["agents.id"], name="history_logs_ibfk_2", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["user_id"], ["users.id"], name="history_logs_ibfk_1", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb4_0900_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "agents",
        sa.Column("id", mysql.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("short_name", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("name", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("description", mysql.TEXT(), nullable=True),
        sa.Column("price", mysql.FLOAT(), nullable=True),
        sa.Column(
            "created_at",
            mysql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            mysql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb4_0900_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "users",
        sa.Column("id", mysql.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("username", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("email", mysql.VARCHAR(length=255), nullable=False),
        sa.Column(
            "created_at",
            mysql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.Column(
            "updated_at",
            mysql.TIMESTAMP(),
            server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
            nullable=True,
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb4_0900_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_index("username", "users", ["username"], unique=True)
    op.create_index("email", "users", ["email"], unique=True)
    op.create_table(
        "historylog",
        sa.Column("id", mysql.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("question", mysql.LONGTEXT(), nullable=False),
        sa.Column("prompt", mysql.LONGTEXT(), nullable=False),
        sa.Column("answer", mysql.LONGTEXT(), nullable=False),
        sa.Column(
            "feedback",
            mysql.VARCHAR(length=7),
            nullable=True,
            comment="LIKE: like\nDISLIKE: dislike",
        ),
        sa.Column("created_at", mysql.DATETIME(fsp=6), nullable=False),
        sa.Column("agent_id", mysql.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("user_id", mysql.INTEGER(), autoincrement=False, nullable=False),
        sa.ForeignKeyConstraint(
            ["agent_id"],
            ["agent.id"],
            name="fk_historyl_agent_369e413d",
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
            name="fk_historyl_user_fd6dfb48",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb4_0900_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "agent",
        sa.Column("id", mysql.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("short_name", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("name", mysql.VARCHAR(length=255), nullable=False),
        sa.Column("description", mysql.LONGTEXT(), nullable=True),
        sa.Column(
            "background_image",
            mysql.VARCHAR(length=200),
            server_default=sa.text("'img.jpg'"),
            nullable=True,
        ),
        sa.Column(
            "profile_image",
            mysql.VARCHAR(length=200),
            server_default=sa.text("'img.jpg'"),
            nullable=True,
        ),
        sa.Column(
            "original_price", mysql.DECIMAL(precision=10, scale=2), nullable=True
        ),
        sa.Column("new_price", mysql.DECIMAL(precision=10, scale=2), nullable=True),
        sa.Column(
            "percentage_discount", mysql.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column("offer_expiration_data", sa.DATE(), nullable=False),
        sa.Column("created_at", mysql.DATETIME(fsp=6), nullable=False),
        sa.Column(
            "updated_at",
            mysql.DATETIME(fsp=6),
            server_default=sa.text(
                "CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)"
            ),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb4_0900_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_table(
        "user",
        sa.Column("id", mysql.INTEGER(), autoincrement=True, nullable=False),
        sa.Column("username", mysql.VARCHAR(length=20), nullable=False),
        sa.Column("email", mysql.VARCHAR(length=200), nullable=False),
        sa.Column("password", mysql.VARCHAR(length=100), nullable=False),
        sa.Column(
            "is_verified",
            mysql.TINYINT(display_width=1),
            server_default=sa.text("'0'"),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("join_date", mysql.DATETIME(fsp=6), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb4_0900_ai_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    op.create_index("username", "user", ["username"], unique=True)
    op.create_index("email", "user", ["email"], unique=True)
    # ### end Alembic commands ###
