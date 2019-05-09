import redis

# host是redis主机，需要启动 ./redis-server
# redis默认port（端口）是6379
# decode_responses=True，写入的键值对中的value为str类型，不加这个参数写入的则为字节类型
# password 需要密码。非同机访问，需要填写密码才可以访问
r = redis.Redis(host='192.168.0.104', port=6379, decode_responses=True, password='fsdfwef32r23r32vsdvvavsfdvsf12e21fav')
# key是"foo" value是"bar" 将键值对存入redis缓存
r.set('foo', 'is foo')
# 取出键foo对应的值，这两种方式都可以
print(r['foo'])
print(r.get('foo'))