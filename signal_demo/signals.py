# Namespace 的作用，为了防止多人开发的时候，信号名字冲突的问题
from blinker import Namespace
from datetime import datetime
from flask import request,g,template_rendered

namespace = Namespace()

login_signal = namespace.signal('login')


# 定义登陆日志函数
def login_log(sender):
    # 记录用户名，login_log函数中传参   登录时间   IP地址
    # 获取时间
    now = datetime.now()
    # 获取ip地址，通过导入request获取
    ip = request.remote_addr
    # 将这些信息组合到log_line中，进行日志的保存
    log_line = "{username}*{now}*{ip}".format(username=g.username,now=now,ip=ip)
    # 打开文件写入信息,了解open函数的运用
    with open('login_log.txt','a') as l:
        l.write(log_line+'\n')
    print('用户登录')
    l= open('login_log.txt','r')
    print(l.read())

login_signal.connect(login_log)