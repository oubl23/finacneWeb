from app import db


class FINANCIAL_ACCOUNT(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String)
    SHORT_NAME = db.Column(db.String)
    REMARK = db.Column(db.String)
    DATA = db.Column(db.String)

    def tojson(self):
        return {
            'ID':str(self.ID),
            'NAME':self.NAME,
            'SHORT_NAME':self.SHORT_NAME,
            'DATA':self.DATA,
            'REMAKR':self.REMARK
        }

    def __str__(self):
        return "id-{} name-{}".format(self.ID,self.NAME.encode('gbk'))

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
            'JOB_ID':self.JOB_ID,
            'ACCOUNT_ID':self.ACCOUNT_ID
        }


