#coding:utf8
import socket,sys,time,os,getpass
import hashlib
def md5sum(filename):
    fHash = ''
    with open(filename, 'rb') as f:
        while True:
            fcont = f.read(102400000)
            if not fcont:
		new=hashlib.md5(fHash)
                return new.hexdigest()
            fpartHash = hashlib.md5(fcont)
            fHash += fpartHash.hexdigest()
try:
    host,g=sys.argv[1:3]
    port=int(g)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
except:
    print "请输入正确的连接地址和端口号并且格式eg:python client.py host port！"
    sys.exit()


print "welcome to XX ftp client!"
login=False
times=0#输入密码错误次数的标记
while 1:
    name=raw_input('input your names:').strip()
    if len(name)==0:
        print "用户名不能为空,请重新输入."
        continue
    for i in xrange(4): 
        if i>=3:
            sys.exit('您的账号已经被锁定,24小时候重新登陆!')
        passwd=getpass.getpass('input your passwd:').strip()
        if len(passwd)==0:
            print "不能输入空的密码,请重新输入."
            continue
        userinfo='%s\t%s'%(name,passwd)
        s.sendall(userinfo)
        log_statu=s.recv(1024)
        if log_statu=='locked':
            sys.exit('您的账号锁定,24小时候后重新登陆!')
        elif log_statu=='passwrong':
            print "密码输入错误请重新输入!"
            continue
        elif log_statu=='nouser':
            print "没有这个用户名!"
            break
        elif log_statu=='true':
            login=True 
            break

    if login==True:

        info='''
                1,put name--上传一个文件到服务器。
                2,get name--下载文件到客户端所在文件夹。
                3,ls--查看服务器端的文件。
                4,del name--删除服务器端的文件
                5,exit--退出客户端程序
                '''
        print info
        while 1:
            buf = ''
            len_data = 0
            time.sleep(0.1)
            comand=raw_input('请输入你的操作:')
            if len(comand)==0:continue
#########get###########
            s.sendall(comand)#请求
            com=comand.split()[:2]
            cmd=com[0]#put or get or ls
            if cmd=='get' and len(com)==2:
                filename=comand.split()[1]#filename
                str_len=s.recv(1024)#先接收文件大小
                if str_len=='no':
                    print "没有这个文件%s或者大小是空."%filename
                    continue
                print str_len
                while 1:
                    str_tmp = s.recv(819600)#本地有一个缓冲区
                    if not len_data:#如果不存在len_data则创建文件并且赋值
                        ofh=open(filename, 'wb+')
                        ofh.close()   
                        len_data=int(str_len)
                    ofh=open(filename, 'ab+')
                    ofh.writelines(str_tmp)
                    ofh.close()   
                    bufsize=os.path.getsize(filename)#文件的大小
                    len_statu=100 * bufsize/len_data
                    print 'recv ratio:'+str(len_statu)+'%'
                    if bufsize==len_data:#如果文件长度=接收到的文件长度
                        s.send('aaaa')
                        print '正在验证MD5请稍候.....'
                        get_md5=s.recv(1024)
                        locmd5=md5sum(filename)
                        if locmd5==get_md5:
                            print "传输完成!server: %s  client:%s"%(get_md5,locmd5)
                            break
                        else:
                            print "文件不完整!..."
                            break
                    
            elif cmd=='put' and len(com)==2:
                time.sleep(0.06)#防止server端阻塞
                filename=comand.split()[1]#filename
                size=os.path.getsize(filename)#传输文件的总大小
                print "文件大小是%s"%size
                with open(filename,'rb') as f:
                    while 1:
                        a=f.read(819600)#一次读取发送byte
                        s.sendall(a)
                        f_size=s.recv(1024)#文件块的大小
                        print 'recv ratio %s' % str(100 * int(f_size)/size)+'%'
                        if (100 * int(f_size)/size)==100:
                            print " 正在验证文件完整性....请稍候..."
                            s.sendall('ok')#确认文件传送完毕      
                            ggg=s.recv(1024)
                            s.sendall(md5sum(filename))#将本地md5传给服务器
                            get_p=s.recv(1024)#最后接收的值
                            if get_p=='ok':
                                print "文件传输成功..."
                            else:
                                print "文件传输失败...类容有丢失!"
                            break
                        
            elif cmd=='del' and len(com)==2:
                p=s.recv(1024)
                print p
            elif cmd=='exit':
                sys.exit()
            elif cmd=='ls':
                time.sleep(0.02)
                tmp1=s.recv(1024)
                print tmp1
            else:
                tmp1=s.recv(1024)
                print tmp1
                print "未知的命令选项,请重新输入..."
                continue
    else:continue            
#print 'congratulations, your file %s has been received successfully, file len%s' % (fn, len_data)
