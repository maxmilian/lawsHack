# -*- coding: utf-8 -*-
import os

def convert_chinese_num_to_en_num(string):
    i = 0
    current = 0
    # print("len: " + str(len(string)))
    while current < len(string):
        if current > 0:
            i *= 10

        ch = string[current:current+1]
        # print("ch: " + ch)
        # print("current: " + str(current))
        if ch == '一':
            i += 1
        elif ch == '1':
            i += 1
        elif ch == '二':
            i += 2
        elif ch == '2':
            i += 2
        elif ch == '三':
            i += 3
        elif ch == '3':
            i += 3
        elif ch == '四':
            i += 4
        elif ch == '4':
            i += 4
        elif ch == '五':
            i += 5
        elif ch == '5':
            i += 5
        elif ch == '六':
            i += 6
        elif ch == '6':
            i += 6
        elif ch == '七':
            i += 7
        elif ch == '7':
            i += 7
        elif ch == '八':
            i += 8
        elif ch == '8':
            i += 8
        elif ch == '九':
            i += 9
        elif ch == '9':
            i += 9
        elif ch == '十':
            if current == 0:
                i += 1
            elif current < len(string) - 1:
                i = int(i / 10)
        elif ch == '○':
            pass
        elif ch == '０':
            pass
        elif ch == '0':
            pass
        else:
            print("no match, string: " + string)

        # print("i: " + str(i))
        current += 1

    return i

def load_files(filename):
    if not os.path.isfile(filename):
        return []

    lists = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            lists.append(line.strip())
    return lists


def process_mongo_year(todo_file, done_file, processor):
    todo_list = load_files(todo_file)
    if len(todo_list) <= 0:
        print(todo_file + ' is not exits or empty')
        exit()

    print('todo: ')
    print(todo_list)

    done_list = load_files(done_file)
    if len(todo_list) <= 0:
        f = open(done_file, "w")
        f.close()

    print('done: ')
    print(done_list)

    for year in todo_list:
        if year in done_list:
            print(str(year) + ' is done')
            continue

        processor(year)

        with open(done_file, 'a+') as f:
            f.write(year + "\n")
            f.close()
