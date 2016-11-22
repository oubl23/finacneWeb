#!/usr/bin/python
# -*- coding: utf-8 -*-

from financeControl import Finance
from itertools import chain
import xlwt
import os,sys,time
import zipfile
import json

# ALI0577.csv ALI0677.csv ALI7789.csv
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
    if isinstance(money,str):
        return float(money.replace(",",""))
    return float(money)

def ali_start_check (filecontent):
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
            line["MONEY"] =   float(line["INCOME"])
        elif line["INCOME"] == '' and line["EXPEND"] != '':
            line["MONEY"] =  float(line["EXPEND"]) * -1
        else:
            line["MONEY"] = 0

def cmc_start_check(data):
    pass

def cmc_stop_check(data):
    return 0

def cmc_data_format(content):
    for line in content:
        line["MONEY"] = float(line["MONEY"].replace("￥","").replace(",",""))

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
            line["MONEY"] =   float(line["INCOME"].replace(",",""))
        elif line["INCOME"] == '' and line["EXPEND"] != '':
            line["MONEY"] =  float(line["EXPEND"].replace(",","")) * -1
        else:
            line["MONEY"] = 0
        #print line["MONEY"]

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
        line["MONEY"] = float(line["MONEY"].replace("元","").replace(",",""))

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
        line["MONEY"] = format_money(line["INCOME"]) - format_money(line["EXPEND"]) + format_money(line["LEND"]) - format_money(line["REPAY"])
        #print line["MONEY"]

#finance = Finance("SWU7814.xlsx","SWU7814", "excel",SWUDATAHEAD, swu_start_check, swu_stop_check, swu_data_format)

# for data in finance.content:
#     for k,v in data.items():
#         print v,
#     print



DATA = {
    "ALI0577.csv":{"type":"csv", "start":ali_start_check,"stop":ali_stop_check,"format":ali_data_format, "DATA":ALIDATAHEAD},
    "ALI0677.csv":{"type":"csv", "start":ali_start_check,"stop":ali_stop_check,"format":ali_data_format, "DATA":ALIDATAHEAD},
    "ALI7789.csv":{"type":"csv", "start":ali_start_check,"stop":ali_stop_check,"format":ali_data_format, "DATA":ALIDATAHEAD},
    "CMC5102.csv":{"type":"csv", "start":cmc_start_check,"stop":cmc_stop_check,"format":cmc_data_format, "DATA":CMCDATAHEAD},
    "CMD0091.csv":{"type":"csv", "start":cmd_start_check,"stop":cmd_stop_check,"format":cmd_data_format, "DATA":CMDDATAHEAD},
    "ICC8451.csv":{"type":"csv", "start":icc_start_check,"stop":icc_stop_check,"format":icc_data_format, "DATA":ICCDATAHEAD},
    "CQA7074.xls":{"type":"excel", "start":cqa_start_check,"stop":cqa_stop_check,"format":cqa_data_format, "DATA":CQADATAHEAD},
    "CQD0403.xls":{"type":"excel", "start":cqd_start_check,"stop":cqd_stop_check,"format":cqd_data_format, "DATA":CQDDATAHEAD},
    "CQD3554.xls":{"type":"excel", "start":cqd_start_check,"stop":cqd_stop_check,"format":cqd_data_format, "DATA":CQDDATAHEAD,"fix":1},
    "CQC1254.xlsx":{"type":"excel", "start":cqc_start_check,"stop":cqc_stop_check,"format":cqc_data_format, "DATA":CQCDATAHEAD},
    "SWU7814.xlsx":{"type":"excel", "start":swu_start_check,"stop":swu_stop_check,"format":swu_data_format, "DATA":SWUDATAHEAD},
}

# open zip file to the fold zip
filename = './static/upload/finance.zip'  #要解压的文件
filedir = './static/data/'  #解压后放入的目录
r = zipfile.is_zipfile(filename)
if r:
    starttime = time.time()
    fz = zipfile.ZipFile(filename,'r')
    for file in fz.namelist():
        fz.extract(file,filedir)

else:
    print('This file is not zip file')

# get data to list
datainall = []
for files,data in DATA.items():
    filename = "./static/data/" + files
    if os.path.exists(filename):
        name = os.path.splitext(files)[0]
        finacne = Finance(filename,name, data["type"], data["DATA"], data["start"], data["stop"], data["format"], fixtable= (data.has_key("fix") if 1 else 0))
        datainall.extend(finacne.content)
        finacne.close_file()
    else:
        print "files no in "

print json.dumps(datainall)
