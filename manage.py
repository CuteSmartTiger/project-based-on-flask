# 迁移脚本
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
from exts import db
from liuhu import create_app
# 此写法有误，from apps.back.models import BACKUser
from apps.back import models as back_models
from apps.front import models as front_models

# 为了方便编写，此步有利于后面简化
BACKUser = back_models.BACKUser
BACKRole = back_models.BACKRole
BACKPermission = back_models.BACKPermission

FrontUser = front_models.FrontUser

# 目的 用法
app = create_app()
manager = Manager(app)
# 此步不可以少，解释原理与作用
Migrate(app,db)
manager.add_command('db',MigrateCommand)


# 通过命令添加后台用户信息
# python manage.py create_back_user -u liuhu -p 1111111 -e liuhu@163.com
@manager.option('-u', '--username',dest='username')
@manager.option('-p', '--password',dest='password')
@manager.option('-e', '--email', dest='email')
# 定义函数
def create_back_user(username,password,email):
    #python manage.py create_back_user -u admin -p 1111111 -e liuhu@163.com，
    # 若写成create back_user少一个下划线则报错
    user = BACKUser(username=username,password=password,email=email)
    # 添加
    db.session.add(user)
    # 提交
    db.session.commit()
    print('back用户添加成功')


# 将用户添加到权限组中,先进行用户判断，在进行角色是判断
@manager.option('-e','--email',dest='email')
@manager.option('-n','--name',dest='name')
def add_user_to_role(email,name):
    # 通过邮箱先查找用户
    user=BACKUser.query.filter_by(email=email).first()
    # 若用户存在
    if user:
        # 用户存在则,判断是否拥有对应的角色
        role = BACKRole.query.filter_by(name=name).first()
        # 若角色存在
        if role:
            # 将用户添加到角色组中，role  users  user 分别指的是
            role.users.append(user)
            db.session.commit()
            print('用户添加角色成功')
        else:
            print('没有这个角色:%s'%name)
    else:
        print('%s没有这个用户'%email)


# 方便通过解释器添加注册用户，方便测试
# - 指定操作简写符，--指定全称操作符，dest 指定操作对象
@manager.option('-t','--telephone',dest='telephone')
@manager.option('-u','--username',dest='username')
@manager.option('-p','--password',dest='password')
def create_front_user(telephone,username,password):
    user = FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(user)
    db.session.commit()



#定义创建角色权限的功能函数，可以使用manage.py create_role进行数据上传的操作
#运行此函数时，将信息添加到BACKRole表中
@manager.command
def create_role():
    # 1.访问者（可以修改个人信息）
    visitor = BACKRole(name='访问者',desc='只能查看数据，不能修改')
    visitor.permissions=BACKPermission.VISITOR

    #2.运营者（修改个人信息，帖子管理 评论  管理前台用户）
    operator = BACKRole(name='运营',desc='修改个人信息，帖子管理 评论  管理前台用户')
    operator.permissions=BACKPermission.VISITOR|BACKPermission.POSTER|BACKPermission.\
        BACKUSER|BACKPermission.FRONTUSER|BACKPermission.COMMENTER

    #3.管理员（拥有大部分权限）
    admin = BACKRole(name='管理员',desc='拥有本系统权限')
    admin.permissions=BACKPermission.VISITOR|BACKPermission.POSTER|\
                      BACKPermission.BACKUSER|BACKPermission.FRONTUSER\
                      |BACKPermission.COMMENTER|BACKPermission.BOARDER

    #4.开发者
    developer = BACKRole(name='开发者',desc='开发者专用角色')
    developer.permissions=BACKPermission.ALL_PERMISSION

    # 提交相关信息,提交多项，使用列表的方式，列表的顺序决定添加信息顺序
    db.session.add_all([visitor,admin,operator,developer])
    db.session.commit()

@manager.command
def test_permission():
    user = BACKUser.query.first()
    # if user.is_developer:
    # if user.has_permissions(BACKPermission.VISITOR):
    if user.has_permissions(BACKPermission.ALL_PERMISSION):
        print('这个用户有访问权限')
    else:
        print('这个用户没有访问权限')




if __name__ == '__main__':
    manager.run()
