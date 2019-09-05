import time
from utils import convert_chinese_num_to_en_num
from citation import get_year_from_mongo

def test_convert_chinese_num_to_en_num():
    string = "九十七"
    integer = 97
    if integer != convert_chinese_num_to_en_num(string):
        print(string + " != " + str(convert_chinese_num_to_en_num(string)))

    string = "十七"
    integer = 17
    if integer != convert_chinese_num_to_en_num(string):
        print(string + " != " + str(convert_chinese_num_to_en_num(string)))

    string = "八十"
    integer = 80
    if integer != convert_chinese_num_to_en_num(string):
        print(string + " != " + str(convert_chinese_num_to_en_num(string)))

    string = "二十四"
    integer = 24
    if integer != convert_chinese_num_to_en_num(string):
        print(string + " != " + str(convert_chinese_num_to_en_num(string)))

    string = "二五三四"
    integer = 2534
    if integer != convert_chinese_num_to_en_num(string):
        print(string + " != " + str(convert_chinese_num_to_en_num(string)))

    string = "九十二"
    integer = 92
    if integer != convert_chinese_num_to_en_num(string):
        print(string + " != " + str(convert_chinese_num_to_en_num(string)))

    string = "三七七○"
    integer = 3770
    if integer != convert_chinese_num_to_en_num(string):
        print(string + " != " + str(convert_chinese_num_to_en_num(string)))

    string = "三四○○"
    integer = 3400
    if integer != convert_chinese_num_to_en_num(string):
        print(string + " != " + str(convert_chinese_num_to_en_num(string)))

    string = "六○五一"
    integer = 6051
    if integer != convert_chinese_num_to_en_num(string):
        print(string + " != " + str(convert_chinese_num_to_en_num(string)))

    string = "八一六"
    integer = 816
    if integer != convert_chinese_num_to_en_num(string):
        print(string + " != " + str(convert_chinese_num_to_en_num(string)))


if __name__== "__main__":
    test_convert_chinese_num_to_en_num()
    # get_year_from_mongo(107)
