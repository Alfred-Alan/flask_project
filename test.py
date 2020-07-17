import pymongo
conn = pymongo.MongoClient('0.0.0.0',port=27017)
db = conn['order']
table = db['user']

res=table.insert_one({'name':1})
print(res)