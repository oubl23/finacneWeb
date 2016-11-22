#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
import xlrd
class Finance(object):
    filename = ''
    name = ''
    type = ''
    file = ''
    DATAHEAD = dict()
    filecontent = ''
    filehead = dict()
    content = []
    excelstart = 0

    def __init__(self,filename, name, type, datahead, start_checker, stop_checker, data_format, fixtable = 0):
        self.filehead = dict()
        self.filecontent = ''
        self.content = []
        self.filename = filename
        self.type = type
        self.DATAHEAD = datahead
        self.__open_file()
        self.name = name
        if type == "csv":
            self.get_table_head_csv(start_checker)
            self.get_table_content_csv(stop_checker)
        elif type == "excel":
            self.excelstart = self.get_table_head_excel(start_checker)
            if fixtable == 1:
                for k,v in self.filehead.items():
                    if v == "EXPEND":
                        self.filehead[k - 1] = v
                        self.filehead.pop(k)
                        break

            self.get_table_content_excel(stop_checker)
        data_format(self.content)

    def __open_file(self):
        if self.type == "csv":
            self.file = file(self.filename, 'rb')
            self.filecontent = csv.reader(self.file)
        elif self.type == 'excel':
            self.file = xlrd.open_workbook(self.filename)
            self.filecontent  = self.file.sheet_by_index(0)

    def close_file(self):
        if self.file == 'csv':
            self.file.close
        elif self.file == 'excel':
            self.file.release_resources()

    def get_table_head_csv(self,checker):
        #if isinstance(checker, int) == False:
        self.csv_data_start(checker=checker)
        for data in self.filecontent:
            for i in range(len(data)):
                if self.DATAHEAD.has_key(self.format_data(data[i])):
                    self.filehead[i] = self.DATAHEAD[self.format_data(data[i])]
            break

    def get_table_content_csv(self, checker):
        for line in self.filecontent:
            #print len(line[0])
            if self.csv_data_stop(line,checker):
                break
            account = dict()
            account["ACCOUNT"] = self.name
            for i in range(len(line)):
                if  self.filehead.has_key(i):
                    account[self.filehead[i]] = self.format_data(line[i])
            self.content.append(account)

    def csv_data_start(self, checker):
        return checker(self.filecontent)

    def csv_data_stop(self, data, checker):
        return checker(data) == 1

    def get_table_head_excel(self, checker):
        for i in range(self.filecontent.nrows):
            if self.excel_data_start(self.filecontent.cell_value(i,0).encode('utf-8').strip() , checker):
                for j in range(self.filecontent.ncols):
                    data = self.filecontent.cell_value(i, j).encode('utf-8').strip()
                    if self.DATAHEAD.has_key(data):
                        self.filehead[j] = self.DATAHEAD[data]
                return i

    def excel_data_start(self, data, checker):
        return checker(data)

    def excel_data_stop(self,data, checker):
        return checker(data)

    def get_table_content_excel(self, checker):
        for i in range(self.excelstart + 1 , self.filecontent.nrows):
            if self.excel_data_stop(self.filecontent.cell_value(i,0), checker):
                continue
            account = dict()
            account["ACCOUNT"] = self.name
            for j in range(self.filecontent.ncols):
                if self.filehead.has_key(j):
                    data = self.format_data_excel(self.filecontent.cell_value(i,j))
                    account[self.filehead[j]] = data
            self.content.append(account)

    def format_data(self, data):
        return data.decode('gbk').encode('utf8').strip()

    def format_data_excel(self,data):
        if isinstance(data, float):
            return int(data)
        else:
            return  data.encode('utf-8').strip()

