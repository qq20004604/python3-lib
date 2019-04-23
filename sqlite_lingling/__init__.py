#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 导入sqlite驱动
import sqlite3
from file_controller_lingling import delete_file


class SQLiteTool(object):
    def __init__(self, *db_name):
        if db_name:
            self.db_name = db_name[0]
        # 游标
        self.c = None
        # 游标
        self.cursor = None

    # with 的时候执行，返回值是 with...as e 中的e的值
    def __enter__(self):
        self.connect(self.db_name)
        return self

    # with 内部代码块执行完毕后执行
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print('Error')
        else:
            self.close()

    # 链接 sqlite 数据库（没有会自动创建）
    def connect(self, db_name):
        self.c = sqlite3.connect(db_name)
        self.cursor = self.c.cursor()

    # 执行 SQL 语句，并返回最后一次查询的查询结果
    def run_sql(self, sql_list):
        # 依次执行 sql 语句
        for sql in sql_list:
            if len(sql) == 1:
                self.cursor.execute(sql[0])
            else:
                self.cursor.execute(*sql)
        return self.cursor.fetchall()

    # 返回 cursor
    def get_cursor(self):
        return self.cursor

    # 当上一次操作是插入时，获取插入的行数
    # 如果是 -1，表示上一次操作不是插入
    def get_insert_rowcount(self):
        return self.cursor.rowcount

    # 关闭连接
    def close(self):
        self.cursor.close()
        self.c.commit()
        self.c.close()


# 测试代码和示例代码
if __name__ == '__main__':
    # 先删除db，确保下面代码可以正常运行
    delete_file('test.db')
    delete_file('test2.db')
    # 创建示例，可以不加 db 的 name，但下面就要手动链接了
    s = SQLiteTool()
    # 虽然可以不加后缀名，或者用其他后缀名，但最好用db后缀吧
    s.connect('test.db')
    # 执行 SQL，如果最后是 select，则返回值是 select 查询的结果，否则为空list，即 []
    # 如果最后的是 insert，可以通过 s.get_insert_rowcount() 获取插入的数据的行数
    result = s.run_sql([
        ['create table user (id varchar(20) primary key, name varchar(20))'],
        ['insert into user (id, name) values (\'1\', \'Michael\'), (\'2\', \'wd\')'],
        ['select * from user']
    ])
    # 打印结果
    print(result)
    # 手动关闭数据库链接
    s.close()

    # 方法二，更简单
    with SQLiteTool("test2.db") as s2:
        # 此时已打开并链接了
        # 执行sql，并拿到返回结果
        s2.run_sql([
            ['create table user (id varchar(20) primary key, name varchar(20))'],
            ['insert into user (id, name) values (\'1\', \'WWW\'), (\'2\', \'DDDD\')']
        ])
        # 得知插入了2行数据，返回值是 2
        print(s2.get_insert_rowcount())
