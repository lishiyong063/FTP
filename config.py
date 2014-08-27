#coding:utf8
import MySQLdb
import time,os,sys
import SocketServer,getpass
class Mysql:
    def __init__(self,host,user,passwd,db):
        self.host=host
        self.user=user
        self.passwd=passwd
        self.db=db
        try:
            self.conn=MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db,port=3306)
            self.cur=self.conn.cursor()
        except:
            print '数据库连接错误'
    def query(self,qtables,qwhere):#查询的功能
        self.qtables=qtables
        self.qwhere=qwhere
        print 'select %s from %s'%(self.qwhere,self.qtables)
        self.cur.execute('select %s from %s'%(self.qwhere,self.qtables))
        self.conn.commit()
        return self.cur.fetchall()
    def new_insert(self,ntable,nwhere,nvalue):#插入的功能
        self.nwhere=nwhere
        self.ntable=ntable
        self.nvalue=nvalue
        sql='insert into %s(%s) values%s'%(self.ntable,self.nwhere,self.nvalue)
        self.cur.execute(sql)
        self.conn.commit()
    def delete(self,dtables,dwhere):
        self.dtables=dtables
        self.dwhere=dwhere
        self.cur.execute('delete from %s where %s '%(self.dtables,self.dwhere))
        self.conn.commit()
    def update(self,utables,ucolumn,uvalues,uwhere):#表 列名 修改的值 条件
        self.utables=utables
        self.uwhere=uwhere
        self.uvalues=uvalues
        self.ucolumn=ucolumn
        print 'update %s set %s=%s where id=%s'%(self.utables,self.ucolumn,self.uvalues,self.uwhere)
        self.cur.execute("update %s set %s='%s' where id=%s"%(self.utables,self.ucolumn,self.uvalues,self.uwhere))
        self.conn.commit()
    def __del__(self):
        self.cur.close()
        self.conn.close()

con=Mysql('localhost','ftp','123.com','ftp')
def exists(user):#判断用户是否存在
    ex_u=con.query("user_info where username='%s'"%user,'id')#得到id的值是多少
    if len(ex_u)==0:
        print "nohava"
        return "no"
    else:
        print "uid"
        print int(ex_u[0][0])
        return int(ex_u[0][0])

#(2L, 'test', '123.com', 0L, '/home/log')
class login:
    home=''
    def login(self,name,passwd,lock=0):#登陆模块登陆3次锁定账号，24小时候自动解锁
      self.name=name
      self.passwd=passwd
      query_u=con.query('user_info','*')
      print query_u
      if lock==True:
          a_cur=str(int(time.time()))
          con.update('user_info','lockedtime',a_cur,int(v[0]))
          return 'lock'  
      for k,v in enumerate(query_u):
        print v[1],'name','self.name',self.name
        if v[1]==self.name:
            print v[1],'name','self.name',self.name
            if int(v[3])!=0:#看锁定的值是不是为0
               print "时间差%s"%(int(time.time())-int(v[3]))
               if int(time.time())-int(v[3])<=36920:
                    return "locked"
               else:
                    con.update(user_info,lockedtime,a_cur,0)
            if v[2]!=self.passwd:
                return "passwrong"
            else:
                self.home=v[4]
                print v[4],'ggggggggggggg'
                return True
      else:
          return 'nouser'
    @classmethod                
    def admin(cls):#管理用户后台
      while 1:
        admin_l=['delete user','add user','modify user','unlock user']
        for i,k in enumerate(admin_l):
            print i+1,k
        what_u=raw_input('please chooser a opration:').strip()
        if what_u=='2':
            a_u=raw_input('请输入要增加的用名字:').strip()
            while 1:
                a_p=raw_input('请输入用户名的密码:').strip()
                a_c=raw_input('再确认一遍输入的密码:').strip()
                if a_p!=a_c:
                    print "两次输入的密码,不一致,请重新输入!"
                    continue
                else:
                    a_h=raw_input("请设定用户的家目录名:").strip()
                    m_h='/root/ftp/'+a_h
                    print m_h
                    con.new_insert('user_info','username,passwd,lockedtime,home',(a_u,a_p,0,m_h))#新插入一行用户数据
                    os.system('mkdir -p %s'%m_h)
                    info='''
                        新增用户信息：
                            username:%s

                            password:%s

                            home-dir:%s
                        '''%(a_u,a_p,a_h)
                    print info
                    break
        elif what_u=='1': #删除用户 
            d_u=raw_input('请输入要删除的用户:')
            a=exists(d_u)
            if a=='no':
                print "没有这个用户存在."
            else:    
                con.delete('user_info',"username='%s'"%d_u)
                print '%s 删除成功.'%d_u
        elif what_u=='3':#修改用户名密码家目录
            m_li=['modify username','modify user-homedir','modify passwd']
            for mi,mk in enumerate(m_li):
                print mi+1,mk
            what_m=raw_input('please choose a opration:').strip()
            while 1:
              what_w=raw_input('Choose to modify a user:').strip()
              what_u=exists(what_w)#存在返回id  不存在返回no
              if what_m=='1':
                 if what_u=='no':
                    print " 这个用户不存在，请重新输入。"
                    continue    
                 else:
                    what_mt=raw_input('请输入要修改的值:').strip()
                    con.update('user_info','username',what_mt,what_u)
                    print "用户名修改成功!"
                    break
              elif what_m=='2':
                 if what_u=='no':
                    print "这个用户不存在，请重新输入。"
                    continue
                 else:
                    what_mt=raw_input('请输入要修改的目录:').strip()
                    what_ho='/var/ftp/'+what_mt
                    con.update('user_info','home',what_ho,what_u)
                    os.system('mkdir -p %s'%update)
                    print "用户主目录修改成功!"
                    break
              elif what_m=='3':
                 if what_u=='no':
                    print "这个用户不存在，请重新输入。"
                    continue
                 else:
                    what_mt=raw_input('请输入要修改的密码:').strip()
                    con.update('user_info','passwd',what_mt,what_u)
                    print "用户名密码修改成功!"
                    break  
              else:
                  print "没有这个选项,你只能选择(1-3)请重新输入！"     
                  continue  
        elif what_u=='4':
          while 1:  
            what_w=raw_input('input to unlock a user:').strip()
            what_u=exists(what_w)
            if what_u=='no':
                print "这个用户不存在，请重新输入。"
                continue
            else:
                what_un=raw_input('你确定要解锁%s吗?(Y/N):')
                if what_un=='Y' or what_un=='y':
                    con.update('user_info','lockedtime',0,what_u)
                    print "用户解锁成功!"
                    break
                elif what_un=='N' or what_un=='n':
                    pass
def filesize(filename):
    os.system('dh -sh %s'%filename)
if __name__=='__main__':
    login.admin()
