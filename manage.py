import json
import shutil
import time
import zipfile

from flask_script import Manager

from app import app, db
from app.models import FINANCIAL_ACCOUNT, FINANCIAL_JOURNAL, Finance_data, FINANCIAL_BALANCE

manager = Manager(app)


@manager.command
def save():
    journal = FINANCIAL_JOURNAL(REMARK="123", MONEY="20", DATE="2016-11-22 00:00:00", JOB_ID="1", REASON="",
                                ACCOUNT_ID="1")
    db.session.merge(journal)
    db.session.commit()

@manager.command
def query_a():
    res = FINANCIAL_ACCOUNT.query.filter_by(ID = 87).first()
    print res


@manager.command
def bulk_save():
    # s = Session()
    objects = [
        FINANCIAL_JOURNAL(REMARK="123", MONEY="20", DATE="2016-11-22 00:00:00", JOB_ID="1", REASON="", ACCOUNT_ID="2"),
        FINANCIAL_JOURNAL(REMARK="123", MONEY="20", DATE="2016-11-22 00:00:00", JOB_ID="1", REASON="", ACCOUNT_ID="3"),
        FINANCIAL_JOURNAL(REMARK="123", MONEY="20", DATE="2016-11-22 00:00:00", JOB_ID="1", REASON="", ACCOUNT_ID="4"),
    ]
    db.session.bulk_save_objects(objects)
    db.session.commit()


@manager.command
def save_from_zip():
    filename = './app/static/upload/finance.zip'
    filedir = './app/static/upload/data'
    r = zipfile.is_zipfile(filename)
    if r:
        fz = zipfile.ZipFile(filename, 'r')
        for file in fz.namelist():
            fz.extract(file, filedir)
        fz.close()
    else:
        print "error"
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
    starttime = time.time()
    for account in financial_accounts:
        if DATA.has_key(account.SHORT_NAME):
            finance_datas = Finance_data(filename=DATA[account.SHORT_NAME]["filename"],
                                         path="./app/static/upload/data/", account_id=account.ID,balance_id=10)
            #finance_datas.save_journal()
        else:
            print "not", account.SHORT_NAME
    print time.time() - starttime
    #shutil.move("./app/static/upload/finance.zip", "./app/static/upload/finance1.zip")


@manager.command
def get_table():
    path = "./app/static/upload/data/"
    finance_data = Finance_data(filename="ALI0577.csv", path=path, account_id="ALI0577")
    finance_data.save_journal()


@manager.command
def query():
    finacnes = FINANCIAL_ACCOUNT.query.all()
    print finacnes


@manager.command
def add_update():
    exists = db.session.query(db.session.query(FINANCIAL_JOURNAL).filter_by(REMARK='123', MONEY="20").exists()).scalar()
    if exists:
        print "exists"
    else:
        finance = FINANCIAL_JOURNAL(REMARK="123", MONEY="20", DATE="2016-11-22 00:00:00", JOB_ID="1", REASON="",
                                    ACCOUNT_ID="4")
        db.session.add(finance)
        db.session.commit()
        print "add"





@manager.command
def query_balance():
    # userList = FINANCIAL_ACCOUNT.query.join(friendships, users.id == friendships.user_id).add_columns(users.userId, users.name,
    #                                                                                       users.email, friends.userId,
    #                                                                                       friendId).filter(
    #     users.id == friendships.friend_id).filter(friendships.user_id == userID).paginate(page, 1, False)
    #fc = db.session.query(FINANCIAL_BALANCE,FINANCIAL_ACCOUNT).join(FINANCIAL_ACCOUNT,FINANCIAL_BALANCE.ACCOUNT_ID == FINANCIAL_ACCOUNT.ID).add_columns(FINANCIAL_ACCOUNT.SHORT_NAME).all()
    fc = db.session.query(FINANCIAL_ACCOUNT,FINANCIAL_BALANCE).join(FINANCIAL_BALANCE,FINANCIAL_ACCOUNT.ID == FINANCIAL_BALANCE.ACCOUNT_ID).all()
    #fc = db.session.query(FINANCIAL_ACCOUNT).join(FINANCIAL_BALANCE).query(
     #   db.func.max(FINANCIAL_BALANCE.DATETIME)).filter_by(ACCOUNT_ID=FINANCIAL_ACCOUNT.ID).all()
    # max = db.session.query(db.func.max(FINANCIAL_BALANCE.DATETIME)).filter_by(ACCOUNT_ID="302").scalar()
    # max_logins = FINANCIAL_BALANCE.query(db.func.max(FINANCIAL_BALANCE.DATETIME)).filter_by(ACCOUNT_ID="500").scalar()
    # for g in fc:
    #     print g
    #print fc
        # users = db.session.query(User).filter(User.numLogins == max_logins).all()
    fc = db.session.query(FINANCIAL_ACCOUNT,db.func.max(FINANCIAL_BALANCE.DATETIME)).outerjoin(FINANCIAL_BALANCE,FINANCIAL_ACCOUNT.ID == FINANCIAL_BALANCE.ACCOUNT_ID).add_columns(FINANCIAL_BALANCE.MONEY).group_by(FINANCIAL_BALANCE.ACCOUNT_ID).all()
    for f in fc:
        account = f.FINANCIAL_ACCOUNT.tojson()
        account["DATETIME"] = str(f[1])
        for x,v in account.items():
            print x,v
        print
        # account = json.dumps(f.FINANCIAL_ACCOUNT.tojson())
        # account = json.loads(account)
        # account.update({"DATETIME":str(f[1])})
        # account = json.dumps(account,sort_keys=True)
        # print account
        #print f.FINANCIAL_ACCOUNT.tojson()


    # session.query(Ip, func.max(Client.ACCOUNT_ID)).
    # outerjoin(ClientIp, ClientIp.ip_id == Ip.id)
@manager.command
def test_buf():
    buf = {}
    if 'blance' in buf:
        print 1
    else:
        print 0


if __name__ == '__main__':
    manager.run()
