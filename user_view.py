from app import *
from tools import MyMongo,host
from flask import Blueprint,jsonify
user = Blueprint("user", __name__)  # 实例化一个蓝图(Blueprint)对象)

# @user.route('/register/',methods=['GET','POST'])
# def show():
#     with MyMongo(path='0.0.0.0', port=27017,db='order',table='user')as c:
#         res=list(c.find({},{'_id':0}))
#         print(res)
#     return jsonify({'code': 200})

@user.route('/login/',methods=['POST'])
def post_login():
    # 用户名
    username = request.form.get('username', None)
    # 用户密码
    password = request.form.get('password', None)
    with MyMongo(path="127.0.0.1", port=27017, db='md', table='user')as c:
        user_list = list(c.find({'username':username,'password':password},{'_id':0}))
        if user_list:
            if int(password) != int(user_list[0]['password']):
                return jsonify({'code': 403, 'message': '登录失败！！！请重新登录'})
            else:
                return jsonify({'code': 200, 'message': '登录成功！！！', 'username': username, 'role': user_list[0]['role']})
        else:
            return jsonify({'code': 403, 'message': '登录失败！！！请重新登录'})
