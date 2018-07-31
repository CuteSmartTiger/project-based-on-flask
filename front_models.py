from exts import db
# 前台用户的主键不使用自增长，目的是防止他人知道用户数量，
# 为了提高用户查找的效率，选择使用shortuuid
import shortuuid
import enum
from datetime import datetime
# 导入产生 及  检查的方法
from werkzeug.security import generate_password_hash,check_password_hash


# 定义枚举类型
class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    SECRET = 3
    UNKNOW = 4


class FrontUser(db.Model):
    __tablename__ = 'front_user'
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid)
    telephone = db.Column(db.String(11),nullable=False,unique=True)
    username = db.Column(db.String(50),nullable=False)
    # 加密后的密码
    _password = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(50),unique=True)
    realname = db.Column(db.String(50))
    avatar = db.Column(db.String(100))
    signature = db.Column(db.String(100))
    # 使用枚举，设定默认值为类下的属性
    gender = db.Column(db.Enum(GenderEnum),default=GenderEnum.UNKNOW)
    # 此处使datetime.now,而不是datetime.now(),实例化对象时会自动计算时间，而后
    # 者在模型创建刚使用时的时间
    join_time = db.Column(db.DateTime,default=datetime.now)

    def __init__(self,*args,**kwargs):
        if "password" in kwargs:
            # kwargs属于字典，这里可以调用字典的内建方法，get，pop,其他内建方法有：
            #调用password函数，返回的self._password
            self.password = kwargs.get('password')
            kwargs.pop("password")
        #super的作用：将除去password的数据提交给父类去处理
        super(FrontUser, self).__init__(*args,**kwargs)

    # 使用装饰器，将函数定义为属性，这里一方面为上面初始化时调用，另一方面为后面给属性增加方法
    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self,rawpwd):
        return check_password_hash(self._password,rawpwd)