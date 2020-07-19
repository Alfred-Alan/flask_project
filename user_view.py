from app import *
from tools import MyMongo
from flask import Blueprint

user = Blueprint("user", __name__)  # 实例化一个蓝图(Blueprint)对象)

# @user.route('/register/',methods=['GET','POST'])
# def show():
#     with MyMongo(path='0.0.0.0',port=27017,db='order',table='user')as c:
#         res=list(c.find({}, {'_id':0}))
#     return jsonify({'code': 200, 'data': res})

