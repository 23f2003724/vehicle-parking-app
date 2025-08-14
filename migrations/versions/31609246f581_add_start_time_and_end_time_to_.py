"""Add start_time and end_time to Reservation

Revision ID: 31609246f581
Revises: 8c502969aaef
Create Date: 2025-07-27 16:16:18.604865
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '31609246f581'
down_revision = '8c502969aaef'
branch_labels = None
depends_on = None

def upgrade():
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column(
                'start_time',
                sa.DateTime(),
                nullable=False,
                server_default=sa.text("'2025-01-01 00:00:00'")
            )
        )
        batch_op.add_column(
            sa.Column(
                'end_time',
                sa.DateTime(),
                nullable=True,
                server_default=sa.text("'2025-01-01 01:00:00'")
            )
        )


def downgrade():
    with op.batch_alter_table('reservation', schema=None) as batch_op:
        batch_op.drop_column('end_time')
        batch_op.drop_column('start_time')
