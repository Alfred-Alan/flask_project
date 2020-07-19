import pickle
import uuid
from app import *
from flask import Blueprint
import tasks
from tools import MyMongo, host
import arrow

order = Blueprint("order", __name__)  # 实例化一个蓝图(Blueprint)对象)

@order.route('/add_order',methods=['GET','POST'])
def add_order():
    print(request.form)
    order_name = request.form.get('order_name')
    order_type = request.form.get('order_type')
    department = request.form.get('department')
    priority = request.form.get('priority')
    use_model = request.form.get('use_model')
    application = request.form.get('application')
    order_info = request.form.get('order_info')
    files = request.files.getlist('file')
    with MyMongo(path=host, port=27017, db='md', table='order')as c:
        # 生成时间对象
        n = arrow.now()
        c.insert_one({
            'id':'',
            'status':'启用',
            'order_type':order_type,
            'accept_department': department,
            'priority': priority,
            'use_model':use_model,
            'application':application,
            'fileList': [],
            'order_info':order_info,
            'create_time': n.format('YYYY-MM-DD HH:mm:ss') ,
            'update_time' :n.format('YYYY-MM-DD HH:mm:ss'),
            'Recipients':'',
            'order_name': order_name,
        })


    if files:
        for file in files:
            p_str = pickle.dumps(file)
            suffix = file.filename[file.filename.rfind('.'):]
            filename = str(uuid.uuid4())+suffix

            file.save('./static/'+filename)
            tasks.upload_file.delay(order_name,str(p_str), filename)

    return jsonify({'code': 200})

