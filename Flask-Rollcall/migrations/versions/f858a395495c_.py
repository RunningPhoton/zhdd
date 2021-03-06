"""empty message

Revision ID: f858a395495c
Revises: 
Create Date: 2018-11-06 19:54:43.804197

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f858a395495c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('name', sa.String(length=20), nullable=True),
    sa.Column('role', sa.Integer(), nullable=True),
    sa.Column('verify', sa.Integer(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=False)
    op.create_index(op.f('ix_users_role'), 'users', ['role'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_table('courses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('code', sa.String(length=30), nullable=True),
    sa.Column('name', sa.String(length=30), nullable=True),
    sa.Column('location', sa.String(length=30), nullable=True),
    sa.Column('time', sa.String(length=50), nullable=True),
    sa.Column('teacher_id', sa.Integer(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['teacher_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_courses_code'), 'courses', ['code'], unique=True)
    op.create_index(op.f('ix_courses_teacher_id'), 'courses', ['teacher_id'], unique=False)
    op.create_table('file',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_file_name'), 'file', ['name'], unique=True)
    op.create_index(op.f('ix_file_user_id'), 'file', ['user_id'], unique=False)
    op.create_table('signs',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('sign_count', sa.Integer(), nullable=True),
    sa.Column('attendance', sa.Integer(), nullable=True),
    sa.Column('expectation', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=False),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_signs_course_id'), 'signs', ['course_id'], unique=False)
    op.create_index(op.f('ix_signs_sign_count'), 'signs', ['sign_count'], unique=False)
    op.create_table('user_courses',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['courses.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_courses_course_id'), 'user_courses', ['course_id'], unique=False)
    op.create_index(op.f('ix_user_courses_student_id'), 'user_courses', ['student_id'], unique=False)
    op.create_table('student_sign',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('student_id', sa.Integer(), nullable=True),
    sa.Column('sign_id', sa.Integer(), nullable=True),
    sa.Column('status', sa.Integer(), nullable=True),
    sa.Column('create_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['sign_id'], ['signs.id'], ),
    sa.ForeignKeyConstraint(['student_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_student_sign_sign_id'), 'student_sign', ['sign_id'], unique=False)
    op.create_index(op.f('ix_student_sign_status'), 'student_sign', ['status'], unique=False)
    op.create_index(op.f('ix_student_sign_student_id'), 'student_sign', ['student_id'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_student_sign_student_id'), table_name='student_sign')
    op.drop_index(op.f('ix_student_sign_status'), table_name='student_sign')
    op.drop_index(op.f('ix_student_sign_sign_id'), table_name='student_sign')
    op.drop_table('student_sign')
    op.drop_index(op.f('ix_user_courses_student_id'), table_name='user_courses')
    op.drop_index(op.f('ix_user_courses_course_id'), table_name='user_courses')
    op.drop_table('user_courses')
    op.drop_index(op.f('ix_signs_sign_count'), table_name='signs')
    op.drop_index(op.f('ix_signs_course_id'), table_name='signs')
    op.drop_table('signs')
    op.drop_index(op.f('ix_file_user_id'), table_name='file')
    op.drop_index(op.f('ix_file_name'), table_name='file')
    op.drop_table('file')
    op.drop_index(op.f('ix_courses_teacher_id'), table_name='courses')
    op.drop_index(op.f('ix_courses_code'), table_name='courses')
    op.drop_table('courses')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_role'), table_name='users')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_table('users')
    # ### end Alembic commands ###
