from sqlalchemy import Integer, Column, String, Boolean, DateTime
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Olympiad(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'olympiads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    date = Column(String, nullable=False)
    href = Column(String, nullable=False)

    def __repr__(self):
        return f'<Olympiad> {self.id} {self.type} {self.date}'
