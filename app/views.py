import datetime
import json
import os
import re
import shutil
import time
import zipfile

from flask import render_template, jsonify
from flask import request
from flask import send_from_directory

from app import app, db
from models import FINANCIAL_ACCOUNT, FINANCIAL_JOURNAL, Finance_data, FINANCIAL_BALANCE

basedir = os.path.abspath(os.path.dirname(__file__)) + "/static/upload/"
ALLOWED_EXTENSIONS = set(['zip'])
DATA = {
    "ALI0577": {"filename": "ALI0577.csv"},
    "ALI0677": {"filename": "ALI0677.csv"},
    "ALI7789": {"filename": "ALI7789.csv"},
    "CMC5102": {"filename": "CMC5102.csv"},
    "CMD0091": {"filename": "CMD0091.csv"},
    "ICC8451": {"filename": "ICC8451.csv"},
    "CQA7074": {"filename": "CQA7074.xls"},
    "CQD0403": {"filename": "CQD0403.xls"},
    "CQD3554": {"filename": "CQD3554.xls"},
    "CQC1254": {"filename": "CQC1254.xlsx"},
    "SWU7814": {"filename": "SWU7814.xlsx"}
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
    # finances = FINANCIAL_ACCOUNT.query.all()
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


@app.route("/save_all_journal")
def save_all_journal():
    filename = './app/static/upload/finance.zip'
    filedir = './app/static/upload/data'
    r = zipfile.is_zipfile(filename)
    result = dict()
    if r:
        fz = zipfile.ZipFile(filename, 'r')
        for file in fz.namelist():
            fz.extract(file, filedir)
        fz.close()
    else:
        return jsonify(static="error", message="not zip file")
    financial_accounts = FINANCIAL_ACCOUNT().query.all()

    noexist = []
    for account in financial_accounts:
        if DATA.has_key(account.SHORT_NAME):
            finance_datas = Finance_data(filename=DATA[account.SHORT_NAME]["filename"],
                                         path="./app/static/upload/data/", account_id=account.ID)
            finance_datas.save_journal()
        else:
            noexist.append(account.SHORT_NAME)

    shutil.rmtree("./app/static/upload/data")
    newfilename = "./app/static/upload/" + time.strftime("%Y%m%d%H%M%S", time.localtime(time.time())) + ".zip"
    shutil.move("./app/static/upload/finance.zip", newfilename)

    return jsonify(status="success", noexist=json.dumps(noexist))


@app.route("/add_balance", methods=["POST", ])
def add_balance():
    if 'file' not in request.files:
        return jsonify(status="error")
    file = request.files['file']
    if file.filename == '':
        return jsonify(statuc="error", infomation="not select file")
    if file and allowed_file(file.filename):
        filename = "finance.zip"
        file.save(os.path.join(basedir, filename))
    else:
        return jsonify(status="error", infomation="file is no allow type")

    form = request.form
    balances = parse_to_dict_vals(form)
    if 'balance' in balances:
        for k, v in balances['balance'].items():
            if v["MONEY"] == '':
                v["MONEY"] = 0
            if v["ACCESSARY"] == '':
                v["ACCESSARY"] = 0
            account = FINANCIAL_ACCOUNT.query.filter_by(ID=int(k)).first()
            if account:
                balance = FINANCIAL_BALANCE(ACCOUNT_ID=int(k), DATETIME=datetime.datetime.now(),
                                            MONEY=float(v["MONEY"]),
                                            ACCESSARY=float(v["ACCESSARY"]), CHECKED=0)
                db.session.add(balance)
                db.session.flush()
                if DATA.has_key(account.SHORT_NAME):
                    finance_data = Finance_data(filename=DATA[account.SHORT_NAME]["filename"],
                                                 path="./app/static/upload/data/", account_id=account.ID,
                                                 balance_id=balance.ID)
                    finance_data.save_journal()
                else:
                    pass
                    # print balance.ID
        db.session.commit()
    return jsonify(status="success")


@app.route('/uploadajax', methods=['POST'])
def upldfile():
    if request.method == 'POST':
        if 'file' not in request.files:
            return jsonify(status="error")
        file = request.files['file']
        if file.filename == '':
            return jsonify(statuc="error", infomation="not select file")
        if file and allowed_file(file.filename):
            filename = "finance.zip"
            file.save(os.path.join(basedir, filename))
            return jsonify(status="suucess")
        else:
            return jsonify(status="error", infomation="file is no allow type")


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.')
