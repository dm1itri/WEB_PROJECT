from datetime import datetime
from sqlalchemy import Integer, Column, String, Boolean, DateTime
from sqlalchemy import orm
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase


class Olympiad(SqlAlchemyBase):
    __tablename__ = 'olympiads'

    id = Column(Integer, primary_key=True, autoincrement=True)
    type = Column(String, nullable=False)
    date = Column(String, nullable=False)
    image = Column(String, nullable=True, default='/static/image/olympiads/base.png')
    href = Column(String, nullable=False)

    def __repr__(self):
        return f'<Olympiad> {self.id} {self.type} {self.date}'
