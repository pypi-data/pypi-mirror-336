#! /usr/bin/env python

'''
读取xlsx或xls文件

pip install xlrd
pip install xlwt
pip install openpyxl
'''

import openpyxl
import os
import xlrd
import csv
from collections.abc import Iterable
from collections.abc import Iterator


class ReadCSVUtil(Iterable):

    def __init__(self, file_name):
        self.filename = file_name
        self.suffix = os.path.splitext(self.filename)[-1][1:].lower() # csv

    def __iter__(self):
        return ReadCSVIterator(self.filename)


# 迭代器 csv
class ReadCSVIterator(Iterator):

    def __init__(self, file_name):
        self.filename = file_name
        self.encoding = "GBK"
        self.row = 0

    def __next__(self):
        try:
            with open(self.filename, 'r', self.encoding) as f:
                data = csv.DictReader(f)
                for row_data in data:
                    self.row += 1
                    # (行号, 行内容)
                    yield (self.row, row_data)
        except Exception:
            raise StopIteration
        raise StopIteration

