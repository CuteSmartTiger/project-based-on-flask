#encoding: utf-8
from sqlalchemy import create_engine,Column,Integer,String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'first_sqlalchemy'
USERNAME = 'root'
PASSWORD = 'root'

# dialect+driver://username:password@host:port/database
DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,password=PASSWORD,host=HOSTNAME,port=PORT,db=DATABASE)

engine = create_engine(DB_URI)

Base = declarative_base(engine)

# Session = sessionmaker(engine)
# session = Session()

session = sessionmaker(engine)()


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer,primary_key=True,autoincrement=True)
    name = Column(String(50))
    age = Column(Integer)
    country = Column(String(50))


    #模式返回方法  获取的内容按照模式输出
    def __str__(self):
        return "<Person(name:%s,age:%s,country:%s)>" % (self.name,self.age,self.country)


# session：会话

# 增
def add_data():
    # 创建对象，也即创建一条数据
    p1 = Person(name='zhiliao1',age=19,country='china')
    p2 = Person(name='zhiliao2',age=20,country='china')
    # 一条数据则
    # session.add(p1)
    session.add_all([p1,p2])
    session.commit()

# 查
def search_data():
    # 查找某个模型对应的那个表中所有的数据：
    # all_person = session.query(Person).all()
    # for p in all_person:
    #     print(p)

    # 使用filter_by来做条件查询
    # all_person = session.query(Person).filter_by(name='liuhu').all()
    # for x in all_person:
    #     print(x)

    # 使用filter来做条件查询，可以编写查询复杂的语句
    # all_person = session.query(Person).filter(Person.name=='zhiliao').all()
    # for x in all_person:
    #     print(x)

    # 使用get方法查找数据，get方法是根据id来查找的，只会返回一条数据或者None
    # person = session.query(Person).get(primary_key)

    # 使用first方法获取结果集中的第一条数据
    person = session.query(Person).first()

    print(person)

# 改
def update_data():
    person = session.query(Person).first()
    person.name = 'ketang'
    session.commit()

# 删
def delete_data():
    person = session.query(Person).first()
    session.delete(person)
    session.commit()


# 定义后运行下面的函数
if __name__ == '__main__':
    # add_data()
    # search_data()
    # update_data()
    delete_data()

