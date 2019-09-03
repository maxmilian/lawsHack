# -*- coding: utf-8 -*-
import sys
import re
import pprint
from pymongo import MongoClient
from utils import load_files

# MONGO_HOST = '13.113.158.197:37017'
MONGO_HOST = 'localhost:37017'
FILENAME = './files/years.txt'
FILENAME_OK = 'years.ok.txt'

def get_year_from_mongo(year):
    conn = MongoClient(MONGO_HOST)
    db = conn.TW_case
    count = db.TW_case.count({"JYEAR": int(year)})
    skip = 0
    limit = 5000

    print('get_year_from_mongo: ' + str(year))

    while (skip < count):
        print('skip: ' + str(skip))
        for case in db.TW_case.find({"JYEAR": int(year)}, {"_id": 1}).skip(skip).limit(limit):
            id = case['_id']
            court = id[:3]
            type = id[3:4]
            #print(id + ' ' + court + ' ' + type)
            db.TW_case.find_one_and_update({'_id': id}, {'$set': {'JCOURT': court, 'JTYPE': type}})

        skip += limit

if __name__== "__main__":
    print('main')

    todo_file = FILENAME
    ok_file = FILENAME_OK

    if len(sys.argv) >= 3:
        split = sys.argv[1]
        offset = sys.argv[2]
        todo_file = todo_file.replace(".txt", "_" + str(split) + "_" + str(offset) + ".txt")
        ok_file = ok_file.replace(".ok.txt", "_" + str(split) + "_" + str(offset) + ".ok.txt")
        print("split: " + str(split) + " offset: " + str(offset))
        print("todo_file: " + todo_file + "\nok_file: " + str(ok_file))

    todo_list = load_files(todo_file)
    if len(todo_list) <= 0:
        print(todo_file + ' is not exits or empty')
        exit()

    print('todo: ')
    print(todo_list)

    done_list = load_files(ok_file)
    if len(todo_list) <= 0:
        f = open(ok_file, "w")
        f.close()

    print('done: ')
    print(done_list)

    for year in todo_list:
        if year in done_list:
            print(str(year) + ' is done')
            continue
        get_year_from_mongo(year)

        with open(ok_file, 'a+') as f:
            f.write(year + "\n")
            f.close()

    print('completed')
