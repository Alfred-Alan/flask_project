import pymongo
conn = pymongo.MongoClient('0.0.0.0',port=27017)
db = conn['md']
table = db['order']

res=list(table.find())
print(res)

# with MyMongo(path=host, port=27017, db='md', table='order')as c:
    # print(list(c.find({})))


    