from app import db
from financeControl import Finance


class FINANCIAL_ACCOUNT(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String)
    SHORT_NAME = db.Column(db.String)
    REMARK = db.Column(db.String)
    DATA = db.Column(db.String)

    def tojson(self):
        return {
            'ID': str(self.ID),
            'NAME': self.NAME,
            'SHORT_NAME': self.SHORT_NAME,
            'DATA': self.DATA,
            'REMAKR': self.REMARK
        }

    def __str__(self):
        return "id-{} name-{}".format(self.ID, self.NAME.encode('gbk'))


class FINANCIAL_JOURNAL(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    DATE = db.Column(db.String)
    ACCOUNT_ID = db.Column(db.Integer)
    MONEY = db.Column(db.Float)
    JOB_ID = db.Column(db.Integer)
    REASON = db.Column(db.String)
    REMARK = db.Column(db.String)

    def tojson(self):
        return {
            'ID': str(self.ID),
            'MONEY': self.MONEY,
            'REMARK': self.REMARK,
            'DATA': self.DATA,
            'REASON': self.REASON,
            'JOB_ID': self.JOB_ID,
            'ACCOUNT_ID': self.ACCOUNT_ID
        }


class Finance_data():
    financial_journal_all = []

    def __init__(self, filename, path, name):
        self.account = filename
        self.finance = Finance(filename=filename, path=path, name=name)
        self.content = self.finance.content
        self.__get_financial_journal()

    def __get_financial_journal(self):
        for line in self.content:
            financial_journal = FINANCIAL_JOURNAL(REMARK=line["REMARK"], MONEY=line["MONEY"],
                                                  DATE="2016-11-22 00:00:00", JOB_ID="0", REASON="", ACCOUNT_ID=0)
            self.financial_journal_all.append(financial_journal)

    def save_journal(self):
        db.session.bulk_save_objects(self.financial_journal_all)
        db.session.commit()
