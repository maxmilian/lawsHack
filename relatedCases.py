# -*- coding: utf-8 -*-
import os
import sys
import re
import pprint
from py2neo import Graph
from pymongo import MongoClient
from utils import convert_chinese_num_to_en_num

MONGO_HOST = '13.113.158.197:37017'
# MONGO_HOST = 'localhost:37017'
FILENAME = './files/years.txt'
FILENAME_OK = 'years.ok.txt'

RE_CITATION_1 = r"(最高|高等|行政)法院(著有)?([○００一二三四五六七八九十0123456789]+)年度?(\S{1,3})字第([○００一二三四五六七八九十0123456789]+)號?(民事|刑事)?(、[○０一二三四五六七八九十0123456789]+年\S{1,3}字第[○０一二三四五六七八九十0123456789]+號)*(著有)?(判例|判決|裁判)?(可資|足資|意旨|要旨)?參照"
RE_CITATION_2 = r"參照(最高|高等|行政)法院(著有)?([○００一二三四五六七八九十0123456789]+)年度?(\S{1,3})字第([○００一二三四五六七八九十0123456789]+)號?(民事|刑事)?(、[○０一二三四五六七八九十0123456789]+年\S{1,3}字第[○０一二三四五六七八九十0123456789]+號)*(著有)?(判例|判決|裁判)?(可資|足資|意旨|要旨)?"

def find_case(JYEAR, JCASE, JNO, JTYPE):
    conn = MongoClient(MONGO_HOST)
    db = conn.TW_case
    # count = db.TW_case.count({"JYEAR": {"$or": [str(JYEAR), int(JYEAR)]}, "JNO": {"$or": [str(JNO), int(JNO)]}, "JCASE": JCASE})
    count = db.TW_case.count({"JYEAR": int(JYEAR), "JNO": int(JNO), "JCASE": JCASE})
    print("count: " + str(count))

def get_year_from_mongo(year):
    conn = MongoClient(MONGO_HOST)
    db = conn.TW_case
    count = db.TW_case.count({"$and":[{"JYEAR": int(year)}, {"JCITATION": {"$exists": True}}]})
    skip = 0
    limit = 1000

    graph = Graph("http://localhost:7474", user="neo4j", password="neo4j")
    # graph = Graph(
    #     host = "localhost", # neo4j 搭载服务器的ip地址，ifconfig可获取到
    #     http_port = 7978, # neo4j 服务器监听的端口号
    #     user = "neo4j",
    #     password = "neo4j"
    # )
    graph.delete_all()
    tx = graph.begin()

    print('get_year_from_mongo: ' + str(year))

    while (skip < count):
        print('skip: ' + str(skip))
        for case in db.TW_case.find({"$and":[{"JYEAR": int(year)}, {"JCITATION": {"$exists": True}}]}).skip(skip).limit(limit):
            id = case['_id']
            citation = case['JCITATION']
            type = case['JTYPE']

            match = re.search(RE_CITATION_1, citation)
            if match is None:
                match = re.search(RE_CITATION_2, citation)

            if match is not None:
                year = match.group(3)
                case = match.group(4)
                no = match.group(5)
                if re.search(r"^\d+$", year) == None:
                    year = convert_chinese_num_to_en_num(year)
                if re.search(r"^\d+$", no) == None:
                    no = convert_chinese_num_to_en_num(no)


                print(str(year) + " " + case + " " + str(no))
                case2 = find_case(year, case, no, type)

                # node_1 = Node("CASE", case)
                # node_2 = Node("CASE", case2)
                # rel = Relationship(node_1, "REFER", node_2)
                # tx.merge(node_1)
                # tx.merge(node_2)
                # tx.merge(rel)
                # tx.commit()

                #db.TW_case.find_one_and_update({'_id': id}, {'$set': {'JCITATION': citation}})
            else:
                print("no match, citation: " + citation)
                pass

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
