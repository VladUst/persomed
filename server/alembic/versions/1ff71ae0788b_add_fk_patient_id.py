"""add_fk_patient_id

Revision ID: 1ff71ae0788b
Revises: e5ffaf9e0e5e
Create Date: 2026-03-11 17:35:43.188200

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1ff71ae0788b'
down_revision: Union[str, Sequence[str], None] = 'e5ffaf9e0e5e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('allergies_indicators', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_allergies_indicators_patient_id', 'patients', ['patient_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('analyzes_docs', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_analyzes_docs_patient_id', 'patients', ['patient_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('diseases_history_docs', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_diseases_history_docs_patient_id', 'patients', ['patient_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('family_history_indicators', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_family_history_indicators_patient_id', 'patients', ['patient_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('general_indicators', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_general_indicators_patient_id', 'patients', ['patient_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('laboratory_indicators', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_laboratory_indicators_patient_id', 'patients', ['patient_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('lifestyle_indicators', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_lifestyle_indicators_patient_id', 'patients', ['patient_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('other_docs', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_other_docs_patient_id', 'patients', ['patient_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('recommendations_docs', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_recommendations_docs_patient_id', 'patients', ['patient_id'], ['id'], ondelete='CASCADE')

    with op.batch_alter_table('vaccinations_indicators', schema=None) as batch_op:
        batch_op.create_foreign_key('fk_vaccinations_indicators_patient_id', 'patients', ['patient_id'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    with op.batch_alter_table('vaccinations_indicators', schema=None) as batch_op:
        batch_op.drop_constraint('fk_vaccinations_indicators_patient_id', type_='foreignkey')

    with op.batch_alter_table('recommendations_docs', schema=None) as batch_op:
        batch_op.drop_constraint('fk_recommendations_docs_patient_id', type_='foreignkey')

    with op.batch_alter_table('other_docs', schema=None) as batch_op:
        batch_op.drop_constraint('fk_other_docs_patient_id', type_='foreignkey')

    with op.batch_alter_table('lifestyle_indicators', schema=None) as batch_op:
        batch_op.drop_constraint('fk_lifestyle_indicators_patient_id', type_='foreignkey')

    with op.batch_alter_table('laboratory_indicators', schema=None) as batch_op:
        batch_op.drop_constraint('fk_laboratory_indicators_patient_id', type_='foreignkey')

    with op.batch_alter_table('general_indicators', schema=None) as batch_op:
        batch_op.drop_constraint('fk_general_indicators_patient_id', type_='foreignkey')

    with op.batch_alter_table('family_history_indicators', schema=None) as batch_op:
        batch_op.drop_constraint('fk_family_history_indicators_patient_id', type_='foreignkey')

    with op.batch_alter_table('diseases_history_docs', schema=None) as batch_op:
        batch_op.drop_constraint('fk_diseases_history_docs_patient_id', type_='foreignkey')

    with op.batch_alter_table('analyzes_docs', schema=None) as batch_op:
        batch_op.drop_constraint('fk_analyzes_docs_patient_id', type_='foreignkey')

    with op.batch_alter_table('allergies_indicators', schema=None) as batch_op:
        batch_op.drop_constraint('fk_allergies_indicators_patient_id', type_='foreignkey')
