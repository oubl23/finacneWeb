from app import db
from financeControl import Finance


class FINANCIAL_ACCOUNT(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String)
    SHORT_NAME = db.Column(db.String)
    REMARK = db.Column(db.String)
    DATA = db.Column(db.String)
    LIMIT = db.Column(db.Integer)
    ACCESSARY = db.Column(db.String)

    def tojson(self):
        return {
            'ID': str(self.ID),
            'NAME': self.NAME,
            'SHORT_NAME': self.SHORT_NAME,
            'DATA': self.DATA,
            'REMAKR': self.REMARK,
            'LIMIT': self.LIMIT,
            'ACCESSARY': self.ACCESSARY
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


class FINANCIAL_BALANCE(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    DATETIME = db.Column(db.DATETIME)
    ACCOUNT_ID = db.Column(db.Integer, db.ForeignKey('FINANCIAL_ACCOUNT.ID'))
    MONEY = db.Column(db.Float)
    CHECKED = db.Column(db.Integer)
    ACCESSARY = db.Column(db.Float)
    BALANCE_ID = db.Column(db.Float)


class Finance_data():
    def __init__(self, filename, path, account_id,balance_id):
        self.financial_journal_all = []
        self.balance_id = balance_id
        self.account = filename
        self.finance = Finance(filename=filename, path=path, nameid=account_id)
        self.content = self.finance.content
        #self.__get_financial_journal()

    def __get_financial_journal(self):
        for line in self.content:
            financial_journal = FINANCIAL_JOURNAL(REMARK=line["REMARK"], MONEY=line["MONEY"],
                                                  DATE=line["DATE"], JOB_ID="0", REASON="", ACCOUNT_ID=line["ACCOUNT"])
            self.financial_journal_all.append(financial_journal)

    def save_journal(self):
        # pass
        # db.session.bulk_save_objects(self.financial_journal_all)
        for line in self.content:
            res = get_or_create(db.session, FINANCIAL_JOURNAL, REMARK=line["REMARK"], MONEY=line["MONEY"],
                                DATE=line["DATE"],
                                JOB_ID="0", REASON="", ACCOUNT_ID=line["ACCOUNT"], BALANCE_ID = self.balance_id)
            # db.session.query(FINANCIAL_BALANCE).join(FINANCIAL_ACCOUNT.SHORT_NAME, FINANCIAL_BALANCE.ACCOUNT_ID == FINANCIAL_ACCOUNT.ID)
            # if not res:
            #     print line["REMARK"].decode('utf8'), line["MONEY"],line["DATE"],line["ACCOUNT"]
        db.session.commit()
        # exists = db.session.query(db.session.query(FINANCIAL_JOURNAL).filter_by(name='John Smith').exists()).scalar()
        # db.session
        # db.session.commit()


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return 0
    else:
        instance = model(**kwargs)
        session.add(instance)
        # session.commit()
        # return instance
