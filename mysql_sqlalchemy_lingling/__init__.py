#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 一些复杂用法参照 https://zhuanlan.zhihu.com/p/27400862

# 导入:
from sqlalchemy import Column, INT, String, create_engine, text
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
						   user='root',
						   password='',
						   host='127.0.0.1',
						   port=3306,
						   database=''):
		# '数据库类型+数据库驱动名称://用户名:口令@机器地址:端口号/数据库名'
		s = '{sql}+{drive}://{user}:{pw}@{host}:{port}/{database}'
		s = s.format(sql=sql, drive=drive, user=user, pw=password, host=host, port=str(port), database=database)
		_engine = create_engine(s)
		self._engine = _engine
		db_session = sessionmaker(bind=_engine)
		self.session = db_session()

	# 关闭链接
	def close(self):
		self.session.close()

	# --------------------------------------
	# 拉取数据（单个）
	# 注意，如果返回多个，则会报错
	def query_one(self, class_prototype, *filters):
		if len(filters) > 0:
			one = self.session.query(class_prototype).filter(*filters).one()
		else:
			one = self.session.query(class_prototype).one()
		return one

	# 拉取数据（全部）
	def query_all(self, class_prototype, *filters):
		if len(filters) > 0:
			items = self.session.query(class_prototype).filter(*filters).all()
		else:
			items = self.session.query(class_prototype).all()
		return items

	# 拉取数据（指定id），这个id是根据 primary_key = True 而定的，通常只能返回一个
	def query_by_primary_key(self, class_prototype, key, *filters):
		if len(filters) > 0:
			one = self.session.query(class_prototype).filter(*filters).get(key)
		else:
			one = self.session.query(class_prototype).get(key)
		return one

	# --------------------------------------
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

	# --------------------------------------
	# 符合过滤器的都删除
	# 支持多个条件
	def delete_byfilters(self, class_prototype, *filters):
		self.session.query(class_prototype).filter(*filters).delete()
		self.session.commit()

	# --------------------------------------
	# 改，根据id筛选出符合条件的，然后修改为指定值（可以只修改一个值）
	def update_by_primary_key(self, class_prototype, result_dict, *filters):
		self.session.query(class_prototype).filter(*filters).update(result_dict)

	# --------------------------------------
	# 创建表格测试
	def run_sql(self, sql, *multiparams):
		# 加上 text() 可以防 sql 注入
		# 如果有返回值，可以通过 返回值.fetchall() 来获取值，是一个 tuple
		return self._engine.execute(text(sql), *multiparams)


if __name__ == '__main__':
	# 创建对象的基类:（这里还是要自己手动声明的，因为要继承）
	Base = declarative_base()


	# 1# 测试代码，插入一个 id=1
	# 定义对象:
	class TableTest(Base):
		# 表的名字:
		__tablename__ = 'test'

		# 表的结构:
		# autoincrement=True 表示主键自增
		# primary_key=True 表示是主键
		id = Column(INT(), autoincrement=True, primary_key=True)
		name = Column(String(255))
		age = Column(INT())


	def show_all(t):
		r = t.query_all(TableTest)
		print('_______显示当前全部_______')
		print("id,  name,   age")
		for i in r:
			print(i.id, i.name, i.age)
		print('_______显示结束_______')
		print('')


	# 初始化，删除 > 0
	with SQLAlchemyTool(user='docker', password='1654879wddgfg', database='docker_test_database') as t:
		t.delete_byfilters(TableTest, TableTest.id > 0)
		print('初始化结束')
		show_all(t)

	# 1# 插入一个
	with SQLAlchemyTool(user='docker', password='1654879wddgfg', database='docker_test_database') as t:
		print("==== 1# 测试代码：\n插入 id=1, name='测试1#' ,age=15")
		t.insert_one(TableTest, id=1, name='测试1#', age=15)
		show_all(t)

	# 2# 测试代码，测试 get(n)
	# 指定固定id查询
	with SQLAlchemyTool(user='docker', password='1654879wddgfg', database='docker_test_database') as t:
		r = t.query_by_primary_key(TableTest, 1)
		print("==== 2# 测试代码：指定 primary_key 查询")
		print("id,  name,   age")
		print(r.id, r.name, r.age)
		print('')

	# 3# 测试代码，删除 id=1
	with SQLAlchemyTool(user='docker', password='1654879wddgfg', database='docker_test_database') as t:
		# 可以同时单个filter，或者多个filter一起用，但【必须用filter】
		print("==== 3# 测试代码：\n删除 id=1，然后查询")
		t.delete_byfilters(TableTest, TableTest.id == 1)
		show_all(t)

	# 4# 测试代码，插入多个
	with SQLAlchemyTool(user='docker', password='1654879wddgfg', database='docker_test_database') as t:
		print(
			"==== 4# 测试代码：\n插入(id=1, name='测试2#-1' ,age=14),"
			" (id=2, name='测试2#-2' ,age=20),"
			" (id=3, name='测试2#-3' ,age=13)"
		)
		t.insert_some(TableTest, (
			{'id': 1, 'name': '测试2#-1', 'age': 14},
			{'id': 2, 'name': '测试2#-2', 'age': 20},
			{'id': 3, 'name': '测试2#-3', 'age': 13}
		))
		show_all(t)

	# 5# 测试代码，请求全部 + 使用filter
	with SQLAlchemyTool(user='docker', password='1654879wddgfg', database='docker_test_database') as t:
		# 可以同时单个filter，或者多个filter一起用，也可以不用filter
		print("==== 5# 测试代码：\n 多个filter联动，查询 id < 8, age < 20")
		r = t.query_all(TableTest, TableTest.id < 8, TableTest.age < 20)
		print("id,  name,   age")
		for i in r:
			print(i.id, i.name, i.age)
		print('')

	# 6# 测试代码，update
	with SQLAlchemyTool(user='docker', password='1654879wddgfg', database='docker_test_database') as t:
		print(
			"==== 6# 测试代码：\n将 (id=3, name='测试2#-3' ,age=13)，更新为 age=23\n"
			"并将id < 3的age值更新为 10"
		)
		t.update_by_primary_key(TableTest, {"age": 23}, TableTest.id == 3)
		t.update_by_primary_key(TableTest, {"age": 10}, TableTest.id < 3)
		show_all(t)


	class TableCreateTest(Base):
		# 表的名字:
		__tablename__ = 'create_test3'

		# 表的结构:
		# autoincrement=True 表示主键自增
		# primary_key=True 表示是主键
		id = Column(INT(), autoincrement=True, primary_key=True)
		first_name = Column(String(255))
		last_name = Column(String(255))
		# name = Column(String(255))
		age = Column(INT())


	def show_all_test3(t):
		r = t.query_all(TableCreateTest)
		print('_______显示当前全部_______')
		print("id,  first_name, last_name,   age")
		for i in r:
			print(i.id, i.first_name, i.last_name, i.age)
		print('_______显示结束_______')
		print('')


	# 7# 测试代码，create table
	with SQLAlchemyTool(user='docker', password='1654879wddgfg', database='docker_test_database') as t:
		t.run_sql(
			'UPDATE create_test3 set first_name = :firstname where age = 20',
			{
				'firstname': 'aaaaaa'
			}
		)
		show_all_test3(t)

		t.run_sql(
			'UPDATE create_test3 set first_name = :firstname where age = 20',
			{
				'firstname': 'fi'
			}
		)
		r2 = t.run_sql(
			'select * from create_test3 where age = :age',
			{
				'age': '20'
			}
		)

		print(r2.fetchall())
