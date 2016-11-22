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
        self.open_file()
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

    def open_file(self):
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

    def GetFileNameAndExt(filename):
        import os
        (filepath, tempfilename) = os.path.split(filename);
        (shotname, extension) = os.path.splitext(tempfilename);
        return shotname, extension


if __name__ == "__main__":
    import os, time,zipfile,json

    ALIDATAHEAD = {
        "交易创建时间": "DATE",
        "金额（元）": "MONEY",
        "备注": "REMARK",
        "资金状态": "STATUS"
    }

    # CMD0091.csv
    CMDDATAHEAD = {
        "交易日期": "DATE",
        "交易时间": "TIME",
        "收入": "INCOME",
        "支出": "EXPEND",
        "交易备注": "REMARK",
    }

    # CMC5102.csv
    CMCDATAHEAD = {
        "交易日期": "DATE",
        "交易摘要": "REMARK",
        "人民币金额": "MONEY",
    }

    # ICC8451.csv
    ICCDATAHEAD = {
        '交易日期': "DATE",
        '摘要': "REMARK",
        "交易金额(收入)": "INCOME",
        "交易金额(支出)": "EXPEND",
    }

    CQDDATAHEAD = {
        "交易日期": "DATE",
        "收入": "INCOME",
        "支出": "EXPEND",
        "摘要": "REMARK"
    }

    CQADATAHEAD = {
        "交易日期": "DATE",
        "收入": "INCOME",
        "支出": "EXPEND",
        "摘要（备": "REMARK"
    }

    CQCDATAHEAD = {
        "入账日期": "DATE",
        "交易金额": "MONEY",
        "交易摘要": "REMARK"
    }

    SWUDATAHEAD = {
        "凭证日期": "DATE",
        "摘要": "REMARK",
        "项目支出": "EXPEND",
        "项目收入": "INCOME",
        "项目借款": "LEND",
        "项目还款": "REPAY"
    }


    def format_money(money):
        if isinstance(money, str):
            return float(money.replace(",", ""))
        return float(money)


    def ali_start_check(filecontent):
        for line in filecontent:
            if line[0][0][0] == '-':
                return 1


    def ali_stop_check(data):
        return data[0][0][0] == '-'


    def ali_data_format(content):
        for content in content:
            if content["STATUS"] == "已收入":
                content["MONEY"] = float(content["MONEY"])
            else:
                content["MONEY"] = float(content["MONEY"]) * -1


    def cmd_start_check(filecontent):
        for line in filecontent:
            if len(line[0]) == 0:
                return 1


    def cmd_stop_check(data):
        return len(data[0]) == 0


    def cmd_data_format(content):
        for line in content:
            if line["EXPEND"] == '' and line["INCOME"] != '':
                line["MONEY"] = float(line["INCOME"])
            elif line["INCOME"] == '' and line["EXPEND"] != '':
                line["MONEY"] = float(line["EXPEND"]) * -1
            else:
                line["MONEY"] = 0


    def cmc_start_check(data):
        pass


    def cmc_stop_check(data):
        return 0


    def cmc_data_format(content):
        for line in content:
            line["MONEY"] = float(line["MONEY"].replace("￥", "").replace(",", ""))


    def icc_start_check(filecontent):
        count = 0
        for line in filecontent:
            if len(line[0]) == 0:
                count += 1
            if count == 3:
                return 1
        return count


    def icc_stop_check(data):
        return len(data[0]) < 10


    def icc_data_format(content):
        for line in content:
            if line["EXPEND"] == '' and line["INCOME"] != '':
                line["MONEY"] = float(line["INCOME"].replace(",", ""))
            elif line["INCOME"] == '' and line["EXPEND"] != '':
                line["MONEY"] = float(line["EXPEND"].replace(",", "")) * -1
            else:
                line["MONEY"] = 0
                # print line["MONEY"]


    def cqd_start_check(data):
        return data == "交易日期"


    def cqd_stop_check(data):
        return 0


    def cqd_data_format(content):
        icc_data_format(content)


    def cqc_start_check(data):
        return 1


    def cqc_stop_check(data):
        return 0


    def cqc_data_format(content):
        for line in content:
            line["MONEY"] = float(line["MONEY"].replace("元", "").replace(",", ""))


    def cqa_start_check(data):
        return data == "交易日期"


    def cqa_stop_check(data):
        return 0


    def cqa_data_format(content):
        cqd_data_format(content)


    def swu_start_check(data):
        return 1


    def swu_stop_check(data):
        return len(data) < 10


    def swu_data_format(content):
        for line in content:
            line["MONEY"] = format_money(line["INCOME"]) - format_money(line["EXPEND"]) + format_money(
                line["LEND"]) - format_money(line["REPAY"])
            # print line["MONEY"]


    DATA = {
        "ALI0577.csv": {"type": "csv", "start": ali_start_check, "stop": ali_stop_check, "format": ali_data_format,
                        "DATA": ALIDATAHEAD},
        "ALI0677.csv": {"type": "csv", "start": ali_start_check, "stop": ali_stop_check, "format": ali_data_format,
                        "DATA": ALIDATAHEAD},
        "ALI7789.csv": {"type": "csv", "start": ali_start_check, "stop": ali_stop_check, "format": ali_data_format,
                        "DATA": ALIDATAHEAD},
        "CMC5102.csv": {"type": "csv", "start": cmc_start_check, "stop": cmc_stop_check, "format": cmc_data_format,
                        "DATA": CMCDATAHEAD},
        "CMD0091.csv": {"type": "csv", "start": cmd_start_check, "stop": cmd_stop_check, "format": cmd_data_format,
                        "DATA": CMDDATAHEAD},
        "ICC8451.csv": {"type": "csv", "start": icc_start_check, "stop": icc_stop_check, "format": icc_data_format,
                        "DATA": ICCDATAHEAD},
        "CQA7074.xls": {"type": "excel", "start": cqa_start_check, "stop": cqa_stop_check, "format": cqa_data_format,
                        "DATA": CQADATAHEAD},
        "CQD0403.xls": {"type": "excel", "start": cqd_start_check, "stop": cqd_stop_check, "format": cqd_data_format,
                        "DATA": CQDDATAHEAD},
        "CQD3554.xls": {"type": "excel", "start": cqd_start_check, "stop": cqd_stop_check, "format": cqd_data_format,
                        "DATA": CQDDATAHEAD, "fix": 1},
        "CQC1254.xlsx": {"type": "excel", "start": cqc_start_check, "stop": cqc_stop_check, "format": cqc_data_format,
                         "DATA": CQCDATAHEAD},
        "SWU7814.xlsx": {"type": "excel", "start": swu_start_check, "stop": swu_stop_check, "format": swu_data_format,
                         "DATA": SWUDATAHEAD},
    }

    # open zip file to the fold zip
    filename = './static/upload/finance.zip'  # 要解压的文件
    filedir = './static/data/'  # 解压后放入的目录
    r = zipfile.is_zipfile(filename)
    if r:
        starttime = time.time()
        fz = zipfile.ZipFile(filename, 'r')
        for file in fz.namelist():
            fz.extract(file, filedir)

    else:
        print('This file is not zip file')

    # get data to list
    datainall = []

    for files, data in DATA.items():
        filename = "./static/data/" + files
        if os.path.exists(filename):
            name = os.path.splitext(files)[0]
            finance = Finance(filename, name, data["type"], data["DATA"], data["start"], data["stop"], data["format"], fixtable=(data.has_key("fix") if 1 else 0))
            datainall.extend(finance.content)
            finance.close_file()
        else:
            print "files no in "

    print json.dumps(datainall)