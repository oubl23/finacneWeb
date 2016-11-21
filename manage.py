from app import app
from app.models import FINANCIAL_ACCOUNT
from flask_script import Manager

manager = Manager(app)

@manager.command
def query():
    finacnes = FINANCIAL_ACCOUNT.query.all()
    for finacne in finacnes:
        print finacne

if __name__ == '__main__':
    manager.run()