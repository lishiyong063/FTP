#coding:utf8
import MySQLdb,os,sys
name,password=sys.argv[1],sys.argv[2]
def creat_db():#创建数据库
    try:
        con=MySQLdb.connect(host='localhost',user=name,passwd=password,port=3306)
        cur=con.cursor()
        sql='''
        create database ftp;
        grant all on *.* to ftp@"%" identified by "123.com";
        '''
        cur.execute(sql)
        cur.close()
        con.close()
        return 'ok'
    except MySQLdb.Error,e:
        #print "Mysql Error %d: %s" % (e.args[0], e.args[1])
        return 'no'

a=creat_db()
if a=='ok':
    os.system('mysql -u%s -p%s ftp < ./ftp.sql'%(name,password))
    print "数据导入成功."
else:
    print "数据导入失败,数据库已经存在"
