#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from mysql_lingling import MySQLTool

user = 'docker'
pw = '1654879wddgfg'
database = 'docker_test_database'

with MySQLTool(user=user, password=pw, database=database) as m2:
    # 执行sql并获得返回结果
    result2 = m2.run_sql([
        # ['insert person(id,name, age) values (20, "李四", 20), (30, "王五", 30)'],
        ['select * from test']
        # [
        #     "CREATE TABLE test5 (idd bigint NOT NULL AUTO_INCREMENT,name varchar(255) DEFAULT NULL,age bigint(20) NOT NULL,PRIMARY KEY (idd)) DEFAULT CHARSET=utf8"
        # ]
        # [
        #     "insert test(idd,name,age)values(5,'李四',10), (10, 'abc', 20)"
        # ]
    ])
    # 打印结果
    print(result2)
    # for i in result2:
    #     print(i)
