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

    def __init__(self, filename, path, account_id):
        self.financial_journal_all = []
        self.account = filename
        self.finance = Finance(filename=filename, path=path, nameid=account_id)
        self.content = self.finance.content
        self.__get_financial_journal()

    def __get_financial_journal(self):
        for line in self.content:
            financial_journal = FINANCIAL_JOURNAL(REMARK=line["REMARK"], MONEY=line["MONEY"],
                                                  DATE=line["DATE"], JOB_ID="0", REASON="", ACCOUNT_ID=line["ACCOUNT"])
            self.financial_journal_all.append(financial_journal)

    def save_journal(self):
        #db.session.bulk_save_objects(self.financial_journal_all)
        #for fins in self.financial_journal_all:
        db.session.bulk_insert_mappings(FINANCIAL_JOURNAL,self.financial_journal_all)
        db.session.commit()
