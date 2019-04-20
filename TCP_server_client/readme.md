## 说明

### 总体描述

server，运行后一直生效。

client无论是在 client close或者在 server close，都会触发关闭。


### server.py

server运行的某些数据可配置。

连接server时，server会发送欢迎字符串 ``Welcome!``。

server 收到 exit 时，会触发 close。

server关闭时，会发送 ``Bye~``，然后 close

close 后，客户端再发送信息不会收到回复信息。

### client.py

client 运行结束后自动关闭。

client 单次最多接收1024字节。

client 发送 e，会自己关闭连接。

client 不允许发送空字符串。

close 后，自动结束