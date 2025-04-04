"""add error logging for convert task

Revision ID: 10b3beffe904
Revises: 76da712b9618
Create Date: 2025-01-30 02:12:57.537567

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '10b3beffe904'
down_revision: Union[str, None] = '76da712b9618'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('convert_mp4_task', sa.Column('error_text', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('convert_mp4_task', 'error_text')
    # ### end Alembic commands ###
