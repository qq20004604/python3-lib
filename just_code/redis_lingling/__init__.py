import redis
from datetime import datetime

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

"""
KeyValueGetter: key-value获取控制器
功能说明：
【请求池】：
1、用户注册的key，将被添加进请求池之中；
2、请求池里的key，会不断判断是否过期，过期后则去Redis或Redis获取最新的值；
3、过期后触发请求，但获取值仍然正常获取原先的默认值，只有请求成功后，才会更新原先的默认值（确保实时性）；
4、过期后，先从Redis获取；无法从Redis获取时，从MySQL获取，并更新到Redis里；
【key】：
1、只有用户注册的key，才有效，否则返回空字符串；
2、维持一个请求池，请求池里的内容将定期从Redis或MySQL里获取；
3、本机缓存每个注册的key，默认过期时间是5000ms；
"""


class KeyValueGetter(object):

    # 初始化函数，常见初始配置是
    # host='localhost',
    # port=6379,
    # decode_responses=True,
    # password=''
    def __int__(self, redis_args, mysql_args):
        self._redis_args = redis_args
        self._mysql_args = mysql_args
        self.kv_pool = {}

    # 注册监听一个key
    # key: key值，必须是string类型
    # default_val: 默认值，必须是string类型，必须设置
    # expire_time：过期时间，默认值为5000（单位ms）
    def register_key(self, key, default_val, expire_time=5000):
        if not isinstance(key, str):
            raise TypeError('key:[%s] is not String' % key)
        if not isinstance(default_val, str):
            raise TypeError('key:[%s] must have default value and typeof default value muse be String!' % key)

        self.kv_pool[key] = {
            'value': default_val,
            'expire_time': expire_time,
            # 最近一次更新时间（单位ms）
            'update_time': datetime.now().timestamp() * 1000
        }

    # 根据key获取value
    def get_value(self, key):
        return self.kv_pool[key]['value']

    # 从redis请求
    def query_redis(self):
        nowtime = datetime.now().timestamp() * 1000
        # 以下 key 将被从 Redis 里更新
        redis_keys = []
        # 以下 key 将被从 MySQL 取出
        mysql_keys = []
        for key in self.kv_pool:
            # 当前时间和上一次更新时间 大于 过期时间
            if nowtime - self.kv_pool[key]['update_time'] > self.kv_pool[key]['expire_time']:
                # 那么将key添加待更新list里
                redis_keys.append(key)
        # 如果没找到需要更新的，则返回
        if len(redis_keys) == 0:
            return
        # 连接redis服务器
        r = redis.Redis(**self._redis_args)
        for key in redis_keys:
            value = r.get(key)
