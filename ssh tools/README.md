#ssh_tools

通过其他py引用ssh_tools.py:

import ssh_tools as t  #导入模块

serverinfo = t.f('aaa.txt') #处理服务器信息的文件aaa.txt，格式（ip 端口 用户名 密码 命令行）一行一个服务器

for i in serverinfo:  #循环服务器处理，也可以写多线程

    i[4] = "uname -a" #可以替换命令行，不用修改文件，直接修改
    
    conn = t.SSH(i)   #实例化
    
    print i[0] + "\n " + conn.command() 打印命令返回值
    

output信息如下：

192.168.0.1
 Linux aaaa 4.4.0-141-generic #167-Ubuntu SMP Wed Dec 5 10:40:15 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux

192.168.0.2
 Linux aaaa 4.4.0-141-generic #167-Ubuntu SMP Wed Dec 5 10:40:15 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux

192.168.0.3
 Linux aaaa 4.4.0-141-generic #167-Ubuntu SMP Wed Dec 5 10:40:15 UTC 2018 x86_64 x86_64 x86_64 GNU/Linux
