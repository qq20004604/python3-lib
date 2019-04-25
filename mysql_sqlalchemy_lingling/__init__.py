#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 导入:
from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# 创建对象的基类:
Base = declarative_base()


# 定义User对象:
class User(Base):
    # 表的名字:
    __tablename__ = 'person'

    # 表的结构:
    id = Column(String(20), primary_key=True)
    name = Column(String(255))
    age = Column(String(20))


# 快速初始化数据库链接
def fast_create_engine(sql='mysql',
                       drive='mysqlconnector',
                       user='test',
                       pw='',
                       host='127.0.0.1',
                       port=3306,
                       database=''):
    # '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
    s = '{sql}+{drive}://{user}:{pw}@{host}:{port}/{database}'
    s = s.format(sql=sql, drive=drive, user=user, pw=pw, host=host, port=str(port), database=database)
    print(s)
    return create_engine(s)


# 初始化数据库连接:
# engine = create_engine('mysql+mysqlconnector://docker:1654879wddgfg@localhost:3306/docker_test_database')
engine = fast_create_engine(user='docker', pw='1654879wddgfg', database='docker_test_database')

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)
# 创建Session:
session = DBSession()
# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
user = session.query(User).all()[0]
# 打印类型和对象的name属性:
print('type:', type(user))
print('id: %s, name: %s, age: %s' % (user.id, user.name, user.age))
# 关闭Session:
session.close()
