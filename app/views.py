import datetime
import json
import os
import shutil
import time
import zipfile

from flask import render_template, jsonify
from flask import request
from flask import send_from_directory

from app import app, db
from models import FINANCIAL_ACCOUNT, FINANCIAL_JOURNAL, Finance_data, FINANCIAL_BALANCE


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
    forms = request.form.get("balance")
    balances = json.loads(forms)
    # print balances['balance']
    for k, v in balances['balance'].items():
        if v["MONEY"] == '':
            v["MONEY"] = 0
        if v["ACCESSARY"] == '':
            v["ACCESSARY"] = 0
        balance = FINANCIAL_BALANCE(ACCOUNT_ID=int(k), DATETIME=datetime.datetime.now(), MONEY=float(v["MONEY"]),
                          ACCESSARY=float(v["ACCESSARY"]), CHECKED = 0)
        db.session.merge(balance)
    db.session.commit()
    return render_template("/index.html")
    # @app.route('/add',methods=["POST",])
    # def add():
    #     form = TodoForm(request.form)
    #     if form.validate():
    #         content = form.content.data
    #         todo = Todo(content=content,time=datetime.now())
    #         todo.save()
    #     todos = Todo.objects.order_by('-time')
    #     return render_template("index.html",todos=todos, form=form)
    #
    # @app.route('/done/<string:todo_id>')
    # def done(todo_id):
    #     form = TodoForm()
    #     todo = Todo.objects.get_or_404(id=todo_id)
    #     todo.status = 1
    #     todo.save()
    #     todos = Todo.objects.order_by('-time')
    #     return render_template("index.html", todos=todos, form=form)
    #
    # @app.route('/undone/<string:todo_id>')
    # def undone(todo_id):
    #     form = TodoForm()
    #     todo = Todo.objects.get_or_404(id=todo_id)
    #     todo.status = 0
    #     todo.save()
    #     todos = Todo.objects.order_by('-time')
    #     return render_template("index.html", todos=todos, form=form)
    #
    # @app.route('/delete/<string:todo_id>')
    # def delete(todo_id):
    #     form = TodoForm()
    #     todo = Todo.objects.get_or_404(id=todo_id)
    #     todo.delete()
    #     todos = Todo.objects.order_by('-time')
    #     return render_template("index.html", todos=todos, form=form)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.errorhandler(404)
def not_found(error):
    return render_template('404.')
