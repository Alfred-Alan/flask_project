import pymongo
import pymysql
import redis
host='0.0.0.0'
# host = "localhost"

class My_mysql:
    def __init__(self, path='localhost', port=3306, user='root', password="", db=None):
        # 记录要操作的文件路径和模式
        self.path = path
        self.port = port
        self.db = db
        self.user = user
        self.password = password

    def __enter__(self):
        # 打开文件
        # self.conn = redis.Redis(self.path, self.port)
        # 返回打开的文件对象引用, 用来给  as 后的变量f赋值
        self.conn = pymysql.connect(host=self.path,port=self.port,user =self.user,password =self.password,db =self.db)
        return self.conn.cursor()

    # 退出方法中，用来实现善后处理工作
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        return True
class MyRedis:
    def __init__(self, path='localhost', port='6379'):
        # 记录要操作的文件路径和模式
        self.path = path
        self.port = port

    def __enter__(self):
        # 打开文件
        self.conn = redis.Redis(self.path, self.port)
        # 返回打开的文件对象引用, 用来给  as 后的变量f赋值
        # self.conn = pymongo.MongoClient(self.path,self.port)
        return self.conn

    # 退出方法中，用来实现善后处理工作
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        return True

class MyMongo:
    def __init__(self, path='localhost', port=27017, db='', table=''):
        # 记录要操作的文件路径和模式
        self.path = path
        self.port = port
        self.db = db
        self.table = table

    def __enter__(self):
        # 打开文件
        # self.conn = redis.Redis(self.path, self.port)
        # 返回打开的文件对象引用, 用来给  as 后的变量f赋值
        self.conn = pymongo.MongoClient(self.path,self.port)
        self.db = self.conn[self.db]
        self.table = self.db[self.table]
        return self.table

    # 退出方法中，用来实现善后处理工作
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.close()
        return True


