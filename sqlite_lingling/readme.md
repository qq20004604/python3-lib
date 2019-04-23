# 说明

## 1、作用

sqlite3 模块的再包装。

简化为：

1. 新建/打开数据库；
2. 执行sql语句并返回结果（可以同时执行多条，方法参照测试和示例代码）；
3. 关闭数据库；

示例1：

```
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
```

示例2：（使用with）

```
with SQLiteTool("test2.db") as s2:
    # 此时已打开并链接了
    # 执行sql，并拿到返回结果
    s2.run_sql([
        ['create table user (id varchar(20) primary key, name varchar(20))'],
        ['insert into user (id, name) values (\'1\', \'WWW\'), (\'2\', \'DDDD\')']
    ])
    # 得知插入了2行数据，返回值是 2
    print(s2.get_insert_rowcount())
```