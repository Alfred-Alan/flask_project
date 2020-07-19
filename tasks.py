import threading
import upyun
from tools import MyMongo
from tools import host

from app import celery


@celery.task
def add(a, b):
    n = a + b
    print(n)
    return n

@celery.task
def upload_file(title,file,name):
	# 实例化又拍云对象
	up = upyun.UpYun('mdsave', 'ljq', 'm3QsiAaLhMvB8owYEwdl1l2atviBVF3U')

	# 上传
	# print(type(file.encode('utf-8')))
	# res = up.put('/%s'%name,file)

	with MyMongo(path=host,port=27017,db='md',table='order')as c:
		res=dict(c.find_one({'order_name':title},{'_id':0}))['fileList']
		img_list=[]
		# 如果存在
		if res:
			img_list=res  # 读取添加
			img_list.append(name)
			c.update_one({'order_name': '测试'}, {'$set': {'fileList': img_list}})
			print('添加')
		else:
			img_list.append(name) # 正常添加
			c.update_one({'order_name': '测试'}, {'$set': {'fileList': img_list}})
			print('新增')
	return '成功'
