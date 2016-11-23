import zipfile

from flask_script import Manager

from app import app, db
from app.models import FINANCIAL_ACCOUNT, FINANCIAL_JOURNAL, Finance_data

manager = Manager(app)


@manager.command
def save():
    journal = FINANCIAL_JOURNAL(REMARK="123", MONEY="20", DATE="2016-11-22 00:00:00", JOB_ID="1", REASON="",
                                ACCOUNT_ID="1")
    db.session.merge(journal)
    db.session.commit()


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
    for account in financial_accounts:
        if DATA.has_key(account.SHORT_NAME):
            finance_datas = Finance_data(filename=DATA[account.SHORT_NAME]["filename"], path="./app/static/upload/data/", account_id=account.ID)
            finance_datas.save_journal()
        else:
            print "not", account.SHORT_NAME


@manager.command
def get_table():
    path = "./app/static/upload/data/"
    finance_data = Finance_data(filename="ALI0577.csv", path=path, account_id="ALI0577")
    finance_data.save_journal()


@manager.command
def query():
    finacnes = FINANCIAL_ACCOUNT.query.get(1)
    print finacnes


if __name__ == '__main__':
    manager.run()
