from sqlalchemy import Column, String, DateTime, Integer, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TransactionModels(Base):
    __tablename__ = 'TransactionModels'
    transaction_id = Column(Integer, primary_key=True, nullable=False)
    amount = Column(Float)
    date_created = Column(DateTime)
    description = Column(String, nullable=False, default=None)
    client = Column(String, nullable=False)

    def __int__(self, *args, **kwargs):
        super(TransactionModels, self).__init__(*args, **kwargs)

    def __repr__(self):
        return f"{self.__class__.__qualname__}(amount={self.amount}, client={self.client}, " \
               f"description={self.description})"

    def to_json(self):
        return {
            'amount': self.amount,
            'description': self.description,
            'client': self.client
        }
