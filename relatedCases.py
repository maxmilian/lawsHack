# -*- coding: utf-8 -*-
import sys
import re
from py2neo import Graph,Node,Relationship
from pymongo import MongoClient
from utils import convert_chinese_num_to_en_num
from utils import process_mongo_year

FILENAME = './files/years.txt'
FILENAME_OK = 'years_relatedCases.ok.txt'
RE_CITAION = r"([○００一二三四五六七八九十0123456789]+)年度?(\S{1,3})字第([○００一二三四五六七八九十0123456789]+)號"

MONGO_HOST = '13.113.158.197:37017'
# MONGO_HOST = 'localhost:37017'
NEO4J_PASSWORD = "neo4j"
# NEO4J_PASSWORD = "EibotiG^ZSDXaVxc"

def get_mongo_collection():
    conn = MongoClient(MONGO_HOST)
    db = conn.TW_case
    return db.TW_case

def add_to_graph(yearcaseno1, id1, yearcaseno2, id2):
    graph = Graph("http://localhost:7474/db/data/", password=NEO4J_PASSWORD)
    # graph.delete_all()

    if id1 is not None:
        node_1 = Node("CASE", yearcaseno=yearcaseno1, id=id1)
    else:
        node_1 = Node("CASE", yearcaseno=yearcaseno1)

    if id2 is not None:
        node_2 = Node("CASE", yearcaseno=yearcaseno2, id=id2)
    else:
        node_2 = Node("CASE", yearcaseno=yearcaseno2)
    rel = Relationship(node_1, "REFER", node_2)

    tx = graph.begin()
    tx.merge(node_1, primary_label='Case', primary_key=('yearcaseno'))
    tx.merge(node_2, primary_label='Case', primary_key=('yearcaseno'))
    tx.merge(rel)
    tx.commit()

def find_refer_case(JYEAR, JCASE, JNO, JTYPE):
    collection = get_mongo_collection()

    # count = collection.count({"JYEAR": {"$or": [str(JYEAR), int(JYEAR)]}, "JNO": {"$or": [str(JNO), int(JNO)]}, "JCASE": JCASE})
    count = collection.count({"JYEAR": int(JYEAR), "JNO": int(JNO), "JCASE": JCASE})
    print("count: " + str(count))
    if count == 0:
        return None

    if count == 1:
        case = collection.find_one({"JYEAR": int(JYEAR), "JNO": int(JNO), "JCASE": JCASE})
        print("1 got it " + case['_id'])
    elif count == 2:
        case = collection.find_one({"JYEAR": int(JYEAR), "JNO": int(JNO), "JCASE": JCASE, "JTYPE": JTYPE})
        print("2 got it " + case['_id'])

    return case

def find_refer_case_and_add_to_graph(yearcaseno, id, type, year, jcase, no):
    if re.search(r"^\d+$", year) == None:
        year = convert_chinese_num_to_en_num(year)
    if re.search(r"^\d+$", no) == None:
        no = convert_chinese_num_to_en_num(no)

    yearcaseno2 = str(year) + jcase + str(no)
    print(yearcaseno2)
    case2 = find_refer_case(year, jcase, no, type)

    if case2 is not None:
        yearcaseno2 = str(case2['JYEAR']) + case2['JCASE'] + str(case2['JNO'])
        id2 = case2['_id']
        add_to_graph(yearcaseno, id, yearcaseno2, id2)
    else:
        add_to_graph(yearcaseno, id, yearcaseno2, None)

    return

def process_year_from_mongo(year):
    collection = get_mongo_collection()
    count = collection.count({"$and":[{"JYEAR": int(year)}, {"JCITATION": {"$exists": True}}]})
    skip = 0
    limit = 1000

    print('process_year_from_mongo: ' + str(year))

    while (skip < count):
        print('skip: ' + str(skip))
        case_list = []

        for case in collection.find({"$and":[{"JYEAR": int(year)}, {"JCITATION": {"$exists": True}}]}, {"_id": 1, "JTYPE": 1, "JYEAR": 1, "JCASE": 1, "JNO": 1, "JCITATION": 1}).skip(skip).limit(limit):
            case_list.append(case)

        for case in case_list:
            id = case['_id']
            type = case['JTYPE']
            yearcaseno = str(case['JYEAR']) + case['JCASE'] + str(case['JNO'])
            citations = case['JCITATION']

            for citation in citations:
                pattern = re.compile(RE_CITAION)
                for match in re.finditer(pattern, citation):
                    year = match.group(1)
                    jcase = match.group(2)
                    no = match.group(3)
                    find_refer_case_and_add_to_graph(yearcaseno, id, type, year, jcase, no)


        skip += limit

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

    process_mongo_year(todo_file, ok_file, process_year_from_mongo)

    print('completed')
