#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 一些复杂用法参照 https://zhuanlan.zhihu.com/p/27400862

# 导入:
from sqlalchemy import Column, INT, String, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


class SQLAlchemyTool(object):
	def __init__(self, **args):
		self.session = None
		# 参数不足2个则直接扔掉，因为至少需要 root 和 password
		# database 可以后面手动通过 use [database名] 来进入
		if not ('user' in args and 'password' in args):
			pass
		else:
			# 超过3个，取传的参数的值
			self.args = args

	# with 的时候执行，返回值是 with...as e 中的e的值
	def __enter__(self):
		self.fast_create_engine(**self.args)
		return self

	# with 内部代码块执行完毕后执行
	def __exit__(self, exc_type, exc_value, traceback):
		if exc_type:
			print('Error')
		else:
			self.close()

	# 快速初始化数据库链接
	def fast_create_engine(self,
						   sql='mysql',
						   drive='mysqlconnector',
						   user='test',
						   password='',
						   host='127.0.0.1',
						   port=3306,
						   database=''):
		# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
		s = '{sql}+{drive}://{user}:{pw}@{host}:{port}/{database}'
		s = s.format(sql=sql, drive=drive, user=user, pw=password, host=host, port=str(port), database=database)
		_engine = create_engine(s)
		db_session = sessionmaker(bind=_engine)
		self.session = db_session()

	# 关闭链接
	def close(self):
		self.session.close()

	# 拉取数据（全部）
	def query_all(self, class_prototype, *filters):
		if len(filters) > 0:
			items = self.session.query(class_prototype).filter(*filters).all()
		else:
			items = self.session.query(class_prototype).all()
		return items

	# 拉取数据（单个）
	# 注意，如果返回多个，则会报错
	def query_one(self, class_prototype, *filters):
		if len(filters) > 0:
			one = self.session.query(class_prototype).filter(*filters).one()
		else:
			one = self.session.query(class_prototype).one()
		return one

	# 拉取数据（指定id），这个id是根据 primary_key = True 而定的，通常只能返回一个
	def query_bykey(self, class_prototype, n, *filters):
		if len(filters) > 0:
			one = self.session.query(class_prototype).filter(*filters).get(n)
		else:
			one = self.session.query(class_prototype).get(n)
		return one

	# 插入一个
	def insert_one(self, class_prototype, **args):
		new_item = class_prototype(**args)
		self.session.add(new_item)
		self.session.commit()

	# 插入多个
	def insert_some(self, class_prototype, items):
		for arg in items:
			self.session.add(class_prototype(**arg))
		self.session.commit()


if __name__ == '__main__':
	# 创建对象的基类:（这里还是要自己手动声明的，因为要继承）
	Base = declarative_base()


	# 1# 测试代码，插入一个
	# 定义对象:
	class TableTest(Base):
		# 表的名字:
		__tablename__ = 'test'

		# 表的结构:
		# autoincrement=True 表示主键自增
		# primary_key=True 表示是主键
		id = Column(INT(), autoincrement=True, primary_key=True)
		name = Column(String(255))
		age = Column(String(20))


	# 插入一个
	with SQLAlchemyTool(user='docker', password='1654879wddgfg', database='docker_test_database') as t:
		print("1#插入 name='测试1#' ,age=15")
		t.insert_one(TableTest, name='测试1#', age=15)

	# 2# 测试代码，插入多个
	with SQLAlchemyTool(user='docker', password='1654879wddgfg', database='docker_test_database') as t:
		print("2#插入 name='测试2#-1' ,age=14和name='测试2#-2' ,age=13")
		t.insert_some(TableTest, (
			{'name': '测试2#-1', 'age': 14},
			{'name': '测试2#-2', 'age': 13}
		))

	# 3# 测试代码，测试 get(n)
	# 指定固定id查询
	with SQLAlchemyTool(user='docker', password='1654879wddgfg', database='docker_test_database') as t:
		r = t.query_bykey(TableTest, 2)
		print("3# 测试代码")
		print(r.id, r.name, r.age)

	# 4# 测试代码，请求全部 + 使用filter
	with SQLAlchemyTool(user='docker', password='1654879wddgfg', database='docker_test_database') as t:
		# 可以同时单个filter，或者多个filter一起用，也可以不用filter
		print("4# 测试代码")
		r = t.query_all(TableTest, TableTest.id < 8, TableTest.age < 30)
		for i in r:
			print(i.id, i.name, i.age)

# 创建Query查询，filter是where条件，最后调用one()返回唯一行，如果调用all()则返回所有行:
# user = session.query(User).all()[0]
# # 打印类型和对象的name属性:
# print('type:', type(user))
# print('id: %s, name: %s, age: %s' % (user.id, user.name, user.age))
