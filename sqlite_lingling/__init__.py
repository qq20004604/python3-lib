#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# 导入sqlite驱动
import sqlite3
from file_controller_lingling import delete_file


class SQLiteTool(object):
    def __init__(self):
        # 游标
        self.c = None
        # 游标
        self.cursor = None

    # 链接 sqlite 数据库（没有会自动创建）
    def connect(self, name):
        self.c = sqlite3.connect(name)
        self.cursor = self.c.cursor()

    # 执行 SQL 语句
    def run_sql(self, sql_list):
        # 依次执行 sql 语句
        for sql in sql_list:
            if len(sql) == 1:
                self.cursor.execute(sql[0])
            else:
                self.cursor.execute(*sql)

    # 获取上一次查询结果
    def get_last_sql_result(self):
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


# 测试代码
if __name__ == '__main__':
    # 先删除db，确保下面代码可以正常运行
    delete_file('test.db')
    s = SQLiteTool()
    # 虽然可以不加db，但最好加个后缀名
    s.connect('test.db')
    s.run_sql([
        ['create table user (id varchar(20) primary key, name varchar(20))'],
        ['insert into user (id, name) values (\'1\', \'Michael\')'],
        ['select * from user where id=?', ('1',)],
        ['insert into user (id, name) values (\'2\', \'wd\')'],
        ['select * from user']
    ])
    print(s.get_last_sql_result())
    s.close()
