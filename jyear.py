from pymongo import MongoClient

MONGO_HOST = 'localhost:37017'

conn = MongoClient(MONGO_HOST)
db = conn.TW_case
for case in db.TW_case.find({"JYEAR": {"$type": 2}}):
    id = case['_id']
    print("id: " + id)
    db.TW_case.find_one_and_update({'_id': id}, {'$set': {'JYEAR': int(case['JYEAR'])}})

print('completed')
