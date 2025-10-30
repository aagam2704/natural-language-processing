from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client['bigdata_project']
coll = db['tweets']
count = coll.count_documents({})
print('count:', count)
for i, doc in enumerate(coll.find().limit(5)):
    print('doc', i+1, doc)
