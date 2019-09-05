from pymongo import MongoClient

MONGO_HOST = 'localhost:37017'

conn = MongoClient(MONGO_HOST)
db = conn.TW_case
for case in db.TW_case.find({"JNO": {"$type": 2}}):
    id = case['_id']
    print("id: " + id)

    if "-" in case['JNO']:
        jno = int(case['JNO'].split("-")[0])
    else:
        jno = int(case['JNO'])

    db.TW_case.find_one_and_update({'_id': id}, {'$set': {'JNO': jno}})

print('completed')
