"""
基于 select 方法的 IO多路复用网络并发
重点代码 !!!
"""
from socket import *
from select import *

# 创建好监听套接字
sockfd = socket()
sockfd.bind(('0.0.0.0',8888))
sockfd.listen(5)

# 与非阻塞IO配合防止传输过程阻塞
sockfd.setblocking(False)

p = poll()
map = {sockfd.fileno():sockfd}
p.register(sockfd, POLLIN)
# 准备IO进行监控
# rlist = [sockfd]
# wlist = []
# xlist = []

# 循环监控IO发生
while True:
    # 开始监控IO
    # 伴随监控的IO的增多,就绪的IO情况也会复杂
    # 分类讨论 分两类  sockfd -- connfd

    events = p.poll()
    for fd,event in events:
        # 有客户端连接
        if fd == sockfd.fileno():
            connfd,addr = map[fd].accept()
            print("Connect from",addr)
            connfd.setblocking(False)
            p.register(connfd,POLLIN)
            map[connfd.fileno()] = connfd

        elif event == POLLIN:
            # 某个客户端发消息给我
            data = map[fd].recv(1024).decode()
            if not data:
                #  客户端退出
                p.unregister(fd)
                map[fd].close()
                del map[fd]
                continue
            print("收到:",data)
            map[fd].send(b'ok')
