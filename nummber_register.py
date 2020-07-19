'''
又是找BUG的一天
班级:1907B
日期:{2020/7/19}
阶段：Python高级

'''

from app import *
from tools import MyMongo, host
from flask import Blueprint


number = Blueprint("number", __name__)  # 实例化一个蓝图(Blueprint)对象)

# 注册
@number.route('/register/', methods=["GET", "POST"])
def reg_num():
    username = request.args.get('username')
    password = request.args.get('password')
    print(username)
    print(password)
    with MyMongo(host, 27017, "md", "user") as m:
        user_list = list(m.find({"username":username}, {'_id': 0}))
        if user_list:
            return jsonify({'code': 201})
        else:
            m.insert_one({'username': username, 'password': password, "role": None})
            return jsonify({'code': 200})

# 领取工单
@number.route('/get_work/', methods=["GET", "POST"])
def get_word():
    # 是否与我有管
    about_me = request.form.get('about_me')
    # 接收部门
    accept_department = request.form.get('accept_department')
    # 优先级
    priority = request.form.get('priority')
    print('我是:', about_me)
    print('accept_department', accept_department)
    print('priority', priority)
    with MyMongo(host, 27017, "md", "order") as m:
        user_list = list(m.find({"username": about_me, 'accept_department': accept_department, 'priority': priority}, {'_id': 0}))
        print(user_list)
        return jsonify({'code': 200, 'data': user_list})












