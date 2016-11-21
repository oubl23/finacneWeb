from app import db


class FINANCIAL_ACCOUNT(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    NAME = db.Column(db.String)

    def __str__(self):
        return "id-{} name-{}".format(self.ID,self.NAME.encode('gbk'))


