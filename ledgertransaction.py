from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship

from base import Base

class LedgerTransaction(Base):
     __tablename__ = 'ledger'

     id = Column(Integer, primary_key=True)
     amount = Column(Float)
     payee = Column(String)
     date = Column(Date)
     ofx_id = Column(Integer, ForeignKey('ofx.id'))
     ofx = relationship("OFXTransaction", uselist=False)

     def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                             self.name, self.fullname, self.password)
