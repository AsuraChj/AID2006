"""
poll 方法示例
"""
from select import *
from socket import *


# 准备点IO
f = open('../day16/test.log')

sockfd = socket()
sockfd.bind(('0.0.0.0',8888))
sockfd.listen(5)

sock = socket(AF_INET,SOCK_DGRAM)
sock.bind(('0.0.0.0',9999))

# 查找字典 与 register的IO对象时刻一直
map = {f.fileno():f,sock.fileno():sock}

# 生成poll
p = poll()
p.register(sock,POLLOUT|POLLERR) # 关注
p.register(f,POLLOUT|POLLERR) # 关注


print("开始监控IO")
events = p.poll()
# events --> [(fileno,evnet),()]
print(events)


