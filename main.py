import sys
import os

from PyQt5 import QtWidgets

from alchemical_model import AlchemicalTableModel
from sqlalchemy.ext.declarative import declarative_base
from ofxparse import OfxParser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from base import Base
from ofxtransaction import OFXTransaction
from ledgertransaction import LedgerTransaction

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, model, session, parent=None):
        QtWidgets.QMainWindow.__init__(self,parent)
        self.model = model
        self.session = session
        self.setAcceptDrops(True)
        self.table = QtWidgets.QTableView()
        self.table.setModel(model)
        self.setCentralWidget(self.table)
        self.tableWidget = self.table

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls()]
        for f in files:
            print(f)
            self.populate_rows(f)
        self.model.refresh()

    def populate_rows(self, file_path):
        with open(file_path, 'rb') as fileobj:
            ofx = OfxParser.parse(fileobj)

        currency = ofx.account.statement.currency
        account_id = ofx.account.account_id
        bank_id = ofx.account.routing_number
        branch_id = ofx.account.branch_id

        ofx_transactions = []
        ledger_transactions = []
        for transaction in ofx.account.statement.transactions:
            ofx_transactions.append(OFXTransaction(
                payee = transaction.payee,
                type = transaction.type,
                date = transaction.date,
                amount = transaction.amount,
                fitid = transaction.id,
                acctid = account_id,
                bankid = bank_id,
                branchid = branch_id,
                memo = transaction.memo
                currency = currency
            ))

        self.session.add_all(ofx_transactions)
        self.session.commit()

def main():
    engine = create_engine('sqlite:///:memory:', echo=True)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    Session.configure(bind=engine)
    session = Session()
    model = AlchemicalTableModel(
        session, #FIXME pass in sqlalchemy session object
        session.query(OFXTransaction), #sql alchemy mapped object
        [ # list of column 4-tuples(header, sqlalchemy column, column name, extra parameters as dict
          # if the sqlalchemy column object is Entity.name, then column name should probably be name,
          # Entity.name is what will be used when setting data, and sorting, 'name' will be used to retrieve the data.
            ('Date', OFXTransaction.date, 'date', {}),
            ('Type', OFXTransaction.type, 'type', {}),
            ('Amount', OFXTransaction.amount, 'amount', {}),
            ('Memo', OFXTransaction.memo, 'memo', {}),
        ])
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow(model, session)
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()