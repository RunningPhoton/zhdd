### 需要安装的环境使用pip install下载，若下载失败，尝试换源以及sudo
例如: sudo pip install Flask
### 数据格式一律为json，详情见api.md
### create_tables为数据库创建表的文件
数据库参数配置再setting.py中
建库后(utf-8)，依次执行
python create_tables.py db init
python create_tables.py db migrate
python create_tables.py db upgrade
若数据库表有字段更新，需要把根目录下migrations删除再重新执行以上操作
### 完成了所有基本功能包括学生以及教师操作
签名函数需要修改rollcal.tools中的方法
### 因为暂不考虑从学校数据库拿学生信息，学生信息由学生端自行注册建立
