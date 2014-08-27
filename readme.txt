#请用root用户运行本程序 server 和client


1.先导入数据库.
 库名：ftp      
 用户名：ftp
 密码:123.com
 手动导入：1.create database ftp; 2.use ftp  3.source ./ftp.sql---[路径视情况而定]
 自动导入(只限于本地虚拟机或者)：先将ftp.sql放在和creatsql同一个目录
        执行：python creatsql.py root passwd(本机root用户和密码)
		
		
		
		注意：用户的家目录是：/root/ftp/username 上传删除文件后可在此目录中查看
2.manager:python config.py:提供四个选项增删改用户信息 还有解锁的功能 ，用户将解锁。
        
3.server :python server.py port (port 指本机要使用的端口号)

4.client ：python client localhost port(localhost 指连接的地址 port 指server端的端口号)


client端 可以多处登陆，有put,get,ls,del 功能分别为（a.put filename:上传到用户家目录一个文件。
                                                b.get filename:从家目录下载到当前文件夹
                                                c.ls：查看家目录的文件
                                                d.del filename：删除家目录的一个文件）filename 指文件名
                                                                                                        
经测试：可以上传大文件数据（2G以上） 而且可验证文件完整性
使用hashlib模块。分块读取文件hash的方式。来验证文件数据的完整性。


用户登陆：可验证是否有这个用户，没有重新输入，登陆成功后，在用户家目录上传下载文件。
密码不能为空，输入三次将锁定，24小时候自动解锁，手动解锁：python config.py  有解锁的选项