#coding:utf8
import SocketServer,sys,commands,time,os
import hashlib,config
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
class FtpHandler(SocketServer.BaseRequestHandler):
    def handle(self):
      i=0  
      while 1:
        login=config.login()  
        loginfo = self.request.recv(1024).strip().split('\t')[:2]#接收客户端的用户信息
        user=loginfo[0]
        passwd=loginfo[1]
        log_statu=login.login(user,passwd)#获取登陆的状态发送给客户端 由客户端来判断是否登陆成功
        if i>=2:
            u_id=config.exists(user)
            config.con.update('user_info','lockedtime',int(time.time()),u_id)
	    break
        i+=1
        if log_statu=='passwrong':
            self.request.sendall('passwrong')
        elif log_statu=='nouser':
            self.request.sendall('nouser')
        elif log_statu=='locked':
            self.request.sendall('locked')
        elif log_statu==True:
            home_dir=login.home
            if os.path.exists(home_dir)==False:
                os.system('mkdir -p %s'%home_dir)
            self.request.sendall('true')
            while 1:
                print "等待命令----------"
                get_data = self.request.recv(1024).strip().split()#等待命令接收
                print get_data,'从客户端接收的参数。。。'
                if len(get_data)>=2:
                    cmd, filename = get_data[:2]#取前两个列表的元素
                    target_file='%s/%s'%(home_dir,filename)#目标文件名
                    if cmd == 'get':
                        len_buf=0
                        if os.path.exists(target_file)==True and os.path.getsize(target_file)!=0:
                            size=os.path.getsize(target_file)#文件的总大小
                            print '正在发送 大小%s的文件'%size
                            self.request.send(str(size))#将要下载的文件大小传值过去
                            time.sleep(0.05)
                            with open(target_file,'rb')as f:
                                while 1:
                                    #if not f.readline():break
                                    a=f.read(819600)#一次读16392byte
                                    if len(a)==0:
                                        g=self.request.recv(1024)
                                        self.request.sendall(md5sum(target_file))   
                                        break
                                    else:    
                                        self.request.sendall(a)
                                        
                        else:
                             self.request.sendall('no')
                    elif cmd == 'put':
                        len_data=0#标记
                        while 1:
                            str_tmp = self.request.recv(819600)#本地有一个缓冲区接收文件块
                            if str_tmp=='ok':
                                self.request.sendall('down')
                                get_md5=self.request.recv(1024)#接shou client MD5
                                locmd5=md5sum(target_file)
                                print "server:%s  client:%s"%(locmd5,get_md5)
                                if locmd5==get_md5:
                                    self.request.sendall('ok')
                                else:
                                    self.request.sendall('no')
                                break
                            if not len_data:#如果不存在len_data则创建文件并且赋值
                                ofh=open(target_file, 'wb+')
                                ofh.writelines(str_tmp)
                                len_data=1
                                ofh.close()
				size=os.path.getsize(target_file)
                                self.request.send(str(size))
                            else:    
                                ofh=open(target_file, 'ab+')
                                ofh.writelines(str_tmp)
                                ofh.close()
                                size=os.path.getsize(target_file)
                                self.request.send(str(size))#文件现在的大小
                                
                    elif cmd == 'del':
                        statu=commands.getstatusoutput('rm -rf %s'%target_file)
                        if statu[0]==0:
                            self.request.sendall('删除%s成功'%get_data[1])
                        else:
                            self.request.sendall("操作错误")
                    else:
                        statu=commands.getstatusoutput(get_data[0])
                        if statu[0]==0:
                            self.request.sendall(statu[1])
                        else:
                            self.request.sendall("操作错误")
                elif len(get_data)<2:
                    print '%s %s'%(get_data[0],home_dir)
                    statu=commands.getstatusoutput('%s %s'%(get_data[0],home_dir))
                    if statu[0]==0 and len(statu[1])!=0:
                        self.request.sendall(statu[1])
                        print statu[1],'命令执行成功.'
                        continue
                    elif len(statu[1])==0:
                        self.request.sendall("NUll") 
                    else:
                        self.request.sendall("false")
                        print '命令执行失败.'
                        continue
if __name__=='__main__':
    g=sys.argv[1]
    host,port = 'localhost',int(g)
    server = SocketServer.ThreadingTCPServer((host,port),FtpHandler)
    server.allow_reuse_address = True#设置一直侦听
    server.serve_forever()


