# -*- coding: utf-8 -*-

import sys
import os
import json
import pymongo
from pymongo import MongoClient

MONGO_HOST = '13.113.158.197:37017'
# MONGO_HOST = 'localhost:37017'

def get_mongo_col():
    conn = MongoClient(MONGO_HOST)
    db = conn.TW_case
    return db.TW_case

def finddata(rootDir):
    ls = os.listdir(rootDir)
    ls.sort()

    mongocol = get_mongo_col()
    for lists in ls:
        path = os.path.join(rootDir, lists)
        if "json" in path:
            print(path)
            with open(path) as f:
                file_data = json.load(f)
                jid = file_data.get('JID')
                file_data['_id'] = jid
                file_data['JYEAR'] = int(file_data['JYEAR'])
                file_data['JCOURT'] = jid[:3]
                file_data['JTYPE'] = jid[3:4]

                if "-" in file_data['JNO']:
                    continue

                file_data['JNO'] = int(file_data['JNO'])
                try:
                    mongocol.insert_one(file_data)
                    print("insert")
                except pymongo.errors.DuplicateKeyError:
                    continue
        elif os.path.isdir(path):
            finddata(path)

if __name__== "__main__":

    print(len(sys.argv))

    if len(sys.argv) < 2:
        print("Please input yearmonth")
        exit()

    yearmonth = sys.argv[1]
    print("yearmonth: " + yearmonth)

    finddata("/home/ubuntu/data/" + yearmonth)
