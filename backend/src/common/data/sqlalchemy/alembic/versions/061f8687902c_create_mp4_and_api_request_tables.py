"""create mp4 and api request tables

Revision ID: 061f8687902c
Revises: 
Create Date: 2025-01-04 20:08:22.571764

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '061f8687902c'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('api_request',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('request_method', sa.String(length=8), nullable=False),
    sa.Column('status_code', sa.Integer(), nullable=False),
    sa.Column('received_at', sa.DateTime(), nullable=False),
    sa.Column('duration_ms', sa.Float(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('convert_mp4_task',
    sa.Column('id', sa.BigInteger(), autoincrement=True, nullable=False),
    sa.Column('key', sa.UUID(), nullable=False),
    sa.Column('status', sa.String(length=16), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_convert_mp4_task_key'), 'convert_mp4_task', ['key'], unique=True)
    op.create_index(op.f('ix_convert_mp4_task_updated_at'), 'convert_mp4_task', ['updated_at'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_convert_mp4_task_updated_at'), table_name='convert_mp4_task')
    op.drop_index(op.f('ix_convert_mp4_task_key'), table_name='convert_mp4_task')
    op.drop_table('convert_mp4_task')
    op.drop_table('api_request')
    # ### end Alembic commands ###
