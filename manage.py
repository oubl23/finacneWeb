from app import app, db
from app.models import FINANCIAL_ACCOUNT, FINANCIAL_JOURNAL, Finance_data
from flask_script import Manager

manager = Manager(app)


@manager.command
def save():
    journal = FINANCIAL_JOURNAL(REMARK="123", MONEY="20", DATE="2016-11-22 00:00:00", JOB_ID="1", REASON="",
                                ACCOUNT_ID="1")
    db.session.add(journal)
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
def get_table():
    path = "./app/static/upload/data/"
    finance_data = Finance_data(filename="ALI0577.csv", path=path, name="ALI0577")
    finance_data.save_journal()


@manager.command
def query():
    finacnes = FINANCIAL_ACCOUNT.query.all()
    for finacne in finacnes:
        print finacne


if __name__ == '__main__':
    manager.run()
