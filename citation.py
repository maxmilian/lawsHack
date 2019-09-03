# -*- coding: utf-8 -*-
import os
import sys
import re
import pprint
from pymongo import MongoClient

MONGO_HOST = '13.113.158.197:37017'
# MONGO_HOST = 'localhost:37017'
FILENAME = './files/years.txt'
FILENAME_OK = 'years.ok.txt'

RE_CITATION_1 = r"(最高|高等|行政)法院(著有)?[○００一二三四五六七八九十0123456789]+年度?\S{1,3}字第[○００一二三四五六七八九十0123456789]+號?(民事|刑事)?(、[○０一二三四五六七八九十0123456789]+年\S{1,3}字第[○０一二三四五六七八九十0123456789]+號)*(著有)?(判例|判決|裁判)?(可資|足資|意旨|要旨)?參照"
RE_CITATION_2 = r"參照(最高|高等|行政)法院(著有)?[○００一二三四五六七八九十0123456789]+年度?\S{1,3}字第[○００一二三四五六七八九十0123456789]+號?(民事|刑事)?(、[○０一二三四五六七八九十0123456789]+年\S{1,3}字第[○０一二三四五六七八九十0123456789]+號)*(著有)?(判例|判決|裁判)?(可資|足資|意旨|要旨)?"

def get_content_from_mongo(id):
    conn = MongoClient(MONGO_HOST)
    db = conn.TW_case
    case = db.TW_case.find_one({"_id": id}, {"JFULL": 1})
    print(case)

def get_year_from_mongo(year):
    conn = MongoClient(MONGO_HOST)
    db = conn.TW_case
    count = db.TW_case.count({"JYEAR": str(year)})
    skip = 0
    limit = 5000

    print('get_year_from_mongo: ' + str(year))

    while (skip < count):
        print('skip: ' + str(skip))
        for case in db.TW_case.find({"JYEAR": str(year)}, {"_id": 1, "JFULL": 1}).skip(skip).limit(limit):
            id = case['_id']
            content = case['JFULL']
            if "參照" in content or "參考" in content:
                content = re.sub(r'\r?\n', '', content)
                x = re.search(RE_CITATION_1, content)
                if x is None:
                    x = re.search(RE_CITATION_2, content)

                if x is not None:
                    citation = x.group()
                    print(id + "\n" + citation)
                    db.TW_case.find_one_and_update({'_id': id}, {'$set': {'JCITATION': citation}})
                else:
                    print(id + "\nno refer")

        skip += limit

def load_files(filename):
    if not os.path.isfile(filename):
        return []

    lists = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            lists.append(line.strip())
    return lists

if __name__== "__main__":

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
