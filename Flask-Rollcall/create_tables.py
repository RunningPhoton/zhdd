# encoding:utf-8

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from rollcall.model import User, Course, UserCourse, Sign, StudentSign, File
from rollcall.utils import app, db
manager = Manager(app)

# 使用Migrate绑定app和db
migrate = Migrate(app, db)

# 添加迁移脚本的命令到manager中
manager.add_command('db', MigrateCommand)

# shell of create tables
# python create_tables.py db init
# python create_tables.py db migrate
# python create_tables.py db upgrade
if __name__ == '__main__':
    manager.run()