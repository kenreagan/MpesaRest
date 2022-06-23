from abc import ABC, abstractmethod
from typing import Dict
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from collections.abc import MutableMapping
from sqlalchemy import select, insert, delete
from MpesaRest.models import TransactionModels


class DatabaseContextManager:
    def __init__(self):
        self.engine = create_engine(
            'sqlite:///main.sqlite'
        )

        self.Session = sessionmaker(
            bind=self.engine
        )

    def __enter__(self):
        self.session = self.Session()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb is not None:
            self.session.rollback()

    def rollback(self):
        self.session.rollback()

    def commit(self):
        self.session.commit()



class DatabaseMapper(MutableMapping):
    def __init__(self):
        self.table = TransactionModels

    def __getitem__(self, item):
        with DatabaseContextManager() as context:
            statement = select(
                self.table
            )
            return context.session.execute(statement).fetchall()

    def __setitem__(self, key: int, value: Dict):
        with DatabaseContextManager() as context:
            statement = insert(
                self.table
            ).where(
                id=key
            ).values(
                **value
            )
            context.session.execute(statement)
            context.session.commit()

    def __delitem__(self, key):
        with DatabaseContextManager() as context:
            instance = delete(
                self.table
            ).where(
                id=key
            ).first()
            context.session.execute(instance)
            context.commit()

    def __len__(self):
        return len([elem for elem in self.__iter__()])

    def __iter__(self):
        with DatabaseContextManager() as context:
            for elements in context.session.query(self.table).all():
                yield  elements


class Validator(ABC):
    """
    Validate Input for accuracy
    """
    def __set_value(self, value):
        self.name = f"_{value}"

    def __set__(self, instance, value):
        self.validate(value)
        setattr(
            instance,
            self.name,
            value
        )

    def __get__(self, instance, owner=None):
        return getattr(instance, self.name)

    @abstractmethod
    def validate(self, value):
        pass
