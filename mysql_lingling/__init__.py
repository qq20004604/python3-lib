#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mysql import connector
from printcolor_lingling import print_testresult

_user = ''
_password = ''
_database = ''
_host = '127.0.0.1'
_port = 3306
_unix_socket = None


def log(msg):
    with open('./log.log', 'a')as f:
        f.write('%s\n' % msg)


class MySQLTool(object):
    def __init__(self, **args):
        self.c = None
        self.cursor = None
        # 参数不足2个则直接扔掉，因为至少需要 root 和 password
        if not ('user' in args and 'password' in args):
            pass
        else:
            # 超过3个，取传的参数的值
            self.args = args

    # 连接到数据库，参数要么传值，要么使用默认值
    # 这里的默认值是从 mysql/connector/abstracts.py 复制来的
    def connect(self,
                user=_user,
                password=_password,
                database=_database,
                host=_host,
                port=_port,
                unix_socket=_unix_socket):
        self.c = connector.connect(user=user,
                                   password=password,
                                   database=database,
                                   host=host,
                                   port=port,
                                   unix_socket=unix_socket)
        self.cursor = self.c.cursor()

    # with 的时候执行，返回值是 with...as e 中的e的值
    def __enter__(self):
        self.connect(**self.args)
        return self

    # with 内部代码块执行完毕后执行
    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type:
            print('Error')
        else:
            self.close()

    # 执行 SQL 语句，并返回最后一次查询的查询结果
    def run_sql(self, sql_list):
        error = False
        try:
            # 依次执行 sql 语句
            for sql in sql_list:
                print('sql: %s', sql)
                if len(sql) == 1:
                    self.cursor.execute(sql[0])
                else:
                    self.cursor.execute(*sql)
            # 这里如果报错，说明操作是比如 create table 之类的操作，返回 None
            result = self.cursor.fetchall()
        except BaseException as e:
            print(e)
            error = True
            log(str(e))
        finally:
            # 如果错误，返回False，其他时候返回结果
            if error:
                return False
            else:
                return result

    # 插入一行
    def insert_row(self, sql, args):
        error = False
        try:
            # 正常情况下，返回值为None
            result = self.cursor.execute(sql, args)
            print(result)
        except BaseException as e:
            error = True
            msg = str(e)
            log(msg)
        finally:
            if error:
                return False
            else:
                return self.get_last_insert_id()

    # 同时插入多行（也可以只插入一行），如果插入错误，会返回False
    # 示例：m.insert_more_rows(
    #             'insert person(name,age) values (%s, %s)',
    #             [('六六六', 666)]
    #         )
    def insert_more_rows(self, sql, args):
        error = False
        try:
            # 正常情况下，返回值为None
            self.cursor.executemany(sql, args)
        except BaseException as e:
            error = True
            msg = str(e)
            log(msg)
        finally:
            if error:
                return False
            else:
                return self.get_last_insert_id()

    # 返回 cursor
    def get_cursor(self):
        return self.cursor

    # 当上一次操作是插入时，获取插入的行数。比如插入一条就是一行
    # 如果是 -1，表示上一次操作不是插入
    def get_insert_rowcount(self):
        return self.cursor.rowcount

    # 获取上一个插入行的id（需要要插入后执行才能正确返回id，否则返回None）
    def get_last_insert_id(self):
        return self.cursor.lastrowid

    # 手动提交事务，部分场景下可能有用
    def commit(self):
        self.c.commit()

    # 关闭连接
    def close(self):
        self.cursor.close()
        self.c.commit()
        self.c.close()


# 测试代码和示例代码
# 以下代码的执行前提是本机有一个 mysql 的容器，这个容器参照这个链接
# https://github.com/qq20004604/docker-learning/tree/master/docker-demo-02-MySQL
if __name__ == '__main__':
    is_error = False
    try:
        # 测试数据
        user = 'docker'
        pw = '1654879wddgfg'
        database = 'docker_test_database'

        # ---- 测试代码2 ----
        # 连接数据库
        with MySQLTool(user=user, password=pw, database=database) as m2:
            # 执行sql并获得返回结果
            result2 = m2.run_sql([
                ['insert person(name, age) values ("李四", 20), ("王五", 30)'],
                ['select * from person']
            ])
            # 打印结果
            print(result2)

        print("——————————————————————")
        # ---- 测试代码1 ----
        m = MySQLTool()
        # 查看mysql容器内 ip，参考这个链接：https://blog.csdn.net/CSDN_duomaomao/article/details/75638544
        m.connect(user=user,
                  password=pw,
                  # host=ip,
                  database=database)
        result = m.insert_more_rows(
            'insert person(name,age) values (%s, %s)',
            [('六六六', 666)]
        )
        if result is False:
            is_error = True

        result2 = m.insert_row(
            'insert person(name,age) values (%s, %s)',
            ('六六六', 666)
        )
        if result is False:
            is_error = True

        m.close()
    except BaseException as e:
        print(e)
        is_error = True
    print_testresult(not is_error, 'MySQLTool')
