from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from base import Base

class OFXTransaction(Base):
    __tablename__ = 'ofx'
    id = Column(Integer, primary_key=True)
    payee = Column(String)
    type = Column(String)
    date = Column(Date)
    amount = Column(Float)
    fitid = Column(Integer)
    bankid = Column(Integer)
    branchid = Column(Integer)
    acctid = Column(Integer)
    memo = Column(String)
    sic = Column(String)
    mcc = Column(String)
    checknum = Column(String)
    currency = Column(String)

    def __repr__(self):
        institution_id = '%s:%s' % (self.bankid, self.branchid) if self.branchid else str(self.bankid)
        return "<OFXTransaction(id='%s:%s:%s', amount='%s', date='%s', type='%s', memo='%s')>" % (
                               institution_id, self.acctid, self.fitid, self.amount, self.date, self.type, self.memo)
