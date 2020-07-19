from app import *
from tools import MyMongo

from flask import Blueprint,jsonify,request

orders = Blueprint('get_order',__name__)

@orders.route('/get_orders',methods=['GET'])
def get_or():
    query = request.args.get('query',None)
    if query:
        query = eval(query)
        if query[1] == '不限':
            with MyMongo(path='127.0.0.1',port=27017,db='md',table='order') as m:
                data = list(m.find({'order_type':query[0],'accept_department':query[3]},{"_id":0}))
                return jsonify({"cdoe":200,"data":data})
        else:
            with MyMongo(path='127.0.0.1',port=27017,db='md',table='order') as m:
                data = list(m.find({'order_type':query[0],'accept_department':query[3],'status':query[1]},{"_id":0}))
                return jsonify({"cdoe":200,"data":data})
    else:
        with MyMongo(path='127.0.0.1',port=27017,db='md',table='order') as m:
            data = list(m.find({},{"_id":0}))
            return jsonify({'code':'200',"data":data})

@orders.route('/get_update',methods=['GET'])
def update_get():
    id = request.args.get("id",None)
    num = request.args.get('num',None)
    with MyMongo(path='127.0.0.1',port=27017,db='md',table='order') as m:
        if num == 1:
            m.update_one({'id':id},{"$set":{"status":"禁用"}})
        else:
            m.update_one({'id':id},{"$set":{"status":"启用"}})
    return jsonify({'code':200})
    