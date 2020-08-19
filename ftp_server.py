"""
文件服务器 服务端程序
"""

from socket import *
from threading import Thread
import os, time

# 全局变量定义地址
HOST = "0.0.0.0"
PORT = 8888
ADDR = (HOST, PORT)

# 文件库位置
FTP = "/home/tarena/FTP/"


# 具体处理客户端请求
class FTPServer(Thread):
    def __init__(self, connfd):
        self.connfd = connfd
        super().__init__()

    def do_list(self):
        # 获取文件列表
        file_list = os.listdir(FTP)
        if not file_list:
            # 文件列表为空
            self.connfd.send(b"FAIL")
            return
        else:
            self.connfd.send(b"OK")
            time.sleep(0.1)
            # 发送文件列表
            files = "\n".join(file_list)
            self.connfd.send(files.encode())

    # 处理上传
    def do_put(self, filename):
        # 判断文件是否存在
        if os.path.exists(FTP + filename):
            self.connfd.send(b"FAIL")
            return
        self.connfd.send(b"OK")
        # 接收文件
        f = open(FTP + filename, 'wb')
        while True:
            data = self.connfd.recv(1024)
            if data == b'##':
                break
            f.write(data)
        f.close()

    # 处理下载
    def do_get(self, filename):
        try:
            f = open(FTP + filename, 'rb')
        except:
            self.connfd.send(b'FAIL')
            return
        self.connfd.send(b'OK')
        # 发送文件
        while True:
            data = f.read(1024)
            if not data:
                break
            self.connfd.send(data)
        f.close()
        time.sleep(0.1)
        self.connfd.send(b"##")

    # 处理客户端   总分模型部分
    def run(self):
        while True:
            # 接收某个客户端的所有请求
            data = self.connfd.recv(1024).decode()
            # print(data)
            if not data or data == 'EXIT':
                break
            elif data == "LIST":
                self.do_list()
            elif data[:3] == "PUT":
                filename = data.split(' ')[-1]
                self.do_put(filename)
            elif data[:3] == "GET":
                filename = data.split(' ')[-1]
                self.do_get(filename)

        self.connfd.close()


# 创建多线程并发模型
def main():
    # 创建tcp套接字
    sock = socket()
    sock.bind(ADDR)
    sock.listen(5)

    print("Listen the port %d..." % PORT)
    while True:
        # 循环接收端连接
        try:
            connfd, addr = sock.accept()
            print("Connect from", addr)
        except KeyboardInterrupt:
            sock.close()
            return

        # 创建新的线程,处理客户端具体请求事务
        t = FTPServer(connfd)
        t.setDaemon(True)
        t.start()


if __name__ == '__main__':
    main()
