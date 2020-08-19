"""
http 请求响应演示
"""
from socket import *

# tcp套接字
s = socket()
s.bind(('0.0.0.0',8000))
s.listen(5)

# 接受浏览器连接
c,addr = s.accept()
data = c.recv(1024 * 10) # 接受http请求
print(data.decode())

# 组织响应格式
html = "HTTP/1.1 200 OK\r\n"
html += "Content-Type:text/html\r\n"
html += "\r\n"
with open("python.html") as f:
    html += f.read()

c.send(html.encode()) # 发送响应给浏览器

c.close()
s.close()