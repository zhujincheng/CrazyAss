import os,sys
import paramiko
import test

t = paramiko.Transport(('192.168.0.125',22))
t.connect(username='zhujincheng',password='452335710')
sftp = paramiko.SFTPClient.from_transport(t)
#sftp.put('F:/项目/项目堡垒机/tracfer.py','/home/zhujincheng/tracfer.py') 
print(123)
while True:
    a=input('io')
    print(a)
    test.test()
t.close() 