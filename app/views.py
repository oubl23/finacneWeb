import datetime
import os
import re
import shutil
import time
import zipfile

from flask import render_template, jsonify
from flask import request
from flask import send_from_directory

from app import app, db
from app.financeControl import Finance
from models import FINANCIAL_ACCOUNT, FINANCIAL_JOURNAL, FINANCIAL_BALANCE

basedir = os.path.abspath(os.path.dirname(__file__)) + "/static/upload/"
ALLOWED_EXTENSIONS = set(['zip'])
DATA = {
    "ALI0577": {"filename": ["ALI0577.csv"]},
    "ALI0677": {"filename": ["ALI0677.csv"]},
    "ALI7789": {"filename": ["ALI7789.csv"]},
    "CMC5102": {"filename": ["CMC5102.csv"]},
    "CMD0091": {"filename": ["CMD0091.csv"]},
    "ICC8451": {"filename": ["ICC8451.csv"]},
    "CQA7074": {"filename": ["CQA7074.xls", "CQA7074.xlsx"]},
    "CQD0403": {"filename": ["CQD0403.xls", "CQD0403.xlsx"]},
    "CQD3554": {"filename": ["CQD3554.xls", "CQD3554.xlsx"]},
    "CQC1254": {"filename": ["CQC1254.xls", "CQC1254.xlsx"]},
    "SWU7814": {"filename": ["SWU7814.xls", "SWU7814.xlsx"]},
    "ABC3829": {"filename": ["ABC3829.xls", "ABC3829.xlsx"]}
}


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def parse_to_dict_val(key, value, dict={}):
    # print {"key":key,"value":value,"dict":dict}
    patt = re.compile(r'(?P<name>.*?)[\[](?P<key>.*?)[\]](?P<remaining>.*?)$')
    matcher = patt.match(key)
    matched = matcher == None
    tmp = (matcher.groupdict() if not matched else {"name": key, "key": '', "remaining": ''})
    # print tmp

    n = str(tmp['name'])
    k = str(tmp['key'])
    r = str(tmp['remaining'])

    if not n in dict:
        dict[n] = {}

    if (len(n) > 0) and (len(k) == 0) and (len(r) == 0):  # For standard flat values and when no more remains
        dict[n] = value
    elif (len(n) > 0) and (len(k) > 0) and (
                len(r) == 0):  # if nothing remains to be done, but we have a key, let's set a value
        dict[n][k] = value
    elif (len(n) > 0) and (len(k) > 0) and (len(r) > 0):
        parse_to_dict_val((k + r), value, dict[n])
    else:
        return {}

    return dict


def parse_to_dict_vals(dictin):
    dictout = {}
    for key, value in dictin.items():
        parse_to_dict_val(key, value, dictout)
    return dictout


@app.route("/", methods=["POST", "GET"])
def index():
    finances = db.session.query(FINANCIAL_ACCOUNT, db.func.max(FINANCIAL_BALANCE.DATETIME)).outerjoin(FINANCIAL_BALANCE,
                                                                                                      FINANCIAL_ACCOUNT.ID == FINANCIAL_BALANCE.ACCOUNT_ID).add_columns(
        FINANCIAL_BALANCE.MONEY).group_by(
        FINANCIAL_BALANCE.ACCOUNT_ID).all()
    accounts = []
    for finance in finances:
        account = finance.FINANCIAL_ACCOUNT.tojson()
        account["DATETIME"] = str(finance[1])
        account["MONEY"] = finance[2]
        accounts.append(account)
    return render_template("index.html", accounts=accounts)


@app.route("/list_account")
def list_account():
    finances = db.session.query(FINANCIAL_ACCOUNT, db.func.max(FINANCIAL_BALANCE.DATETIME)).outerjoin(FINANCIAL_BALANCE,
                                                                                                      FINANCIAL_ACCOUNT.ID == FINANCIAL_BALANCE.ACCOUNT_ID).add_columns(
        FINANCIAL_BALANCE.MONEY).group_by(
        FINANCIAL_BALANCE.ACCOUNT_ID).all()
    accounts = []
    for finance in finances:
        account = finance.FINANCIAL_ACCOUNT.tojson()
        account["DATETIME"] = str(finance[1])
        account["MONEY"] = finance[2]
        accounts.append(account)
    # return jsonify(status="success", finances=[finance.FINANCIAL_ACCOUNT.tojson() for finance in finances])
    return jsonify(status="success", accounts=accounts)


@app.route("/save_journal")
def save_journal():
    form = request.form
    journal = FINANCIAL_JOURNAL(ID=form["ID"])
    db.session.add(journal)
    db.commit()


# @app.route("/save_all_journal")
# def save_all_journal():
#     filename = './app/static/upload/finance.zip'
#     filedir = './app/static/upload/data'
#     r = zipfile.is_zipfile(filename)
#     result = dict()
#     if r:
#         fz = zipfile.ZipFile(filename, 'r')
#         for file in fz.namelist():
#             fz.extract(file, filedir)
#         fz.close()
#     else:
#         return jsonify(static="error", message="not zip file")
#     financial_accounts = FINANCIAL_ACCOUNT().query.all()
#
#     noexist = []
#     for account in financial_accounts:
#         if DATA.has_key(account.SHORT_NAME):
#             try:
#                 finance_datas = Finance_data(filename=DATA[account.SHORT_NAME]["filename"],
#                                          path="./app/static/upload/data/", account_id=account.ID)
#             except:
#                 pass
#             finance_datas.save_journal()
#         else:
#             noexist.append(account.SHORT_NAME)
#
#     shutil.rmtree("./app/static/upload/data")
#     newfilename = "./app/static/upload/" + time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + ".zip"
#     shutil.move("./app/static/upload/finance.zip", newfilename)
#
#     return jsonify(status="success", noexist=json.dumps(noexist))


@app.route("/add_balance", methods=["POST", ])
def add_balance():
    if 'file' not in request.files:
        return jsonify(status="error")
    file = request.files['file']
    if file.filename == '':
        return jsonify(status="error", infomation="not select file")
    if file and allowed_file(file.filename):
        filename = "finance.zip"
        file.save(os.path.join(basedir, filename))
        filename = './app/static/upload/finance.zip'
        filedir = './app/static/upload/data'
        r = zipfile.is_zipfile(filename)
        if r:
            fz = zipfile.ZipFile(filename, 'r')
            for file in fz.namelist():
                fz.extract(file, filedir)
            fz.close()
        else:
            return jsonify(status="error", message="not zip file")
    else:
        return jsonify(status="error", infomation="file is no allow type")

    form = request.form
    balances = parse_to_dict_vals(form)
    notexist = []
    erroraccount = []
    if 'balance' not in balances:
        return jsonify(status="error", message="form didn't input success")

    financial_accounts = FINANCIAL_ACCOUNT().query.all()

    message = ""
    add_balances = dict()
    finance_content = dict()
    for financial_account in financial_accounts:
        if not DATA.has_key(financial_account.SHORT_NAME):
            message += financial_account.SHORT_NAME
        else:
            if str(financial_account.ID) not in balances['balance'] and "LACK":
                return jsonify(status="error", message="submit form error")

            if "LACK" in balances['balance'][str(financial_account.ID)] and \
                            balances['balance'][str(financial_account.ID)]["LACK"] == "on":
                continue
            else:
                filename = ""
                for name in DATA[financial_account.SHORT_NAME]["filename"]:
                    filename_check = "./app/static/upload/data/" + name
                    if os.path.exists(filename_check):
                        filename = financial_account.SHORT_NAME
                        add_balances[financial_account.ID] = balances['balance'][str(financial_account.ID)]
                        try:
                            finance = Finance(financial_account.SHORT_NAME, financial_account.ID, filename_check)
                        except Exception, e:
                            app.logger.debug(Exception, e)
                            app.logger.error("conver to " + filename_check + "data error")
                            continue
                        finance_content[financial_account.ID] = finance.content
                        break
                if filename == "":
                    message += financial_account.SHORT_NAME + ","

    # if message != '':
    #     app.logger.error( message + "file error")
    #     return jsonify(status="error",message="submit file error "+message)


    get_data_error = ""
    for k, v in add_balances.items():
        if v["MONEY"] == '':
            v["MONEY"] = 0
        if v["ACCESSARY"] == '':
            v["ACCESSARY"] = 0
        account = FINANCIAL_ACCOUNT.query.filter_by(ID=int(k)).first()

        if account:
            if financial_account.has_key(int(account.ID)):
                balance = FINANCIAL_BALANCE(ACCOUNT_ID=int(k), DATETIME=datetime.datetime.now(),
                                            MONEY=float(v["MONEY"]),
                                            ACCESSARY=float(v["ACCESSARY"]), CHECKED=0)
                db.session.add(balance)
                db.session.flush()
                for line in financial_account[int(account.ID)]:
                    res = get_or_create(db.session, FINANCIAL_JOURNAL, balance.ID, REMARK=line["REMARK"],
                                        MONEY=line["MONEY"],
                                        DATE=line["DATE"],
                                        JOB_ID="0", REASON="", ACCOUNT_ID=line["ACCOUNT"])
    db.session.commit()
    shutil.rmtree("./app/static/upload/data")
    newfilename = "./app/static/upload/" + time.strftime("%Y%m%d%H%M%S",
                                                         time.localtime(time.time())) + ".zip"
    shutil.move("./app/static/upload/finance.zip", newfilename)
    return jsonify(status="success", message="import balance error " + get_data_error)
    #
    # if DATA.has_key(account.SHORT_NAME):
    #     filename = "./app/static/upload/data/" + DATA[account.SHORT_NAME]["filename"]
    #     if os.path.exists(filename):
    #         try:
    #             finance_data = Finance_data(filename=DATA[account.SHORT_NAME]["filename"],
    #                                         path="./app/static/upload/data/", account_id=account.ID)
    #         except :
    #             get_data_error += account.SHORT_NAME + ""
    #             continue
    #         balance = FINANCIAL_BALANCE(ACCOUNT_ID=int(k), DATETIME=datetime.datetime.now(),
    #                                     MONEY=float(v["MONEY"]),
    #                                     ACCESSARY=float(v["ACCESSARY"]), CHECKED=0)
    #         db.session.add(balance)
    #         db.session.flush()
    #
    #         finance_data.save_journal(balance_id=balance.ID)
    #     else:
    #         notexist.append(account.SHORT_NAME)
    # else:
    #     erroraccount.append(int(k))
    #     # print balance.ID


# @app.route('/uploadajax', methods=['POST'])
# def upldfile():
#     if request.method == 'POST':
#         if 'file' not in request.files:
#             return jsonify(status="error")
#         file = request.files['file']
#         if file.filename == '':
#             return jsonify(statuc="error", infomation="not select file")
#         if file and allowed_file(file.filename):
#             filename = "finance.zip"
#             file.save(os.path.join(basedir, filename))
#             return jsonify(status="suucess")
#         else:
#             return jsonify(status="error", infomation="file is no allow type")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def not_found(error):
    return render_template('/404.html')


def get_and_check(session, model, content):
    for line in content:
        res = query(REMARK=line["REMARK"], MONEY=line["MONEY"], DATE=line["DATE"], JOB_ID="0", REASON="",
                    ACCOUNT_ID=line["ACCOUNT"])
        if not res:
            del(line)


def query(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return False
    else:
        return True


def get_or_create(session, model, balance_id, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return False
    else:
        instance = model(BALANCE_ID=balance_id, **kwargs)
        session.add(instance)
        return True
