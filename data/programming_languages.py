from sqlalchemy import Integer, Column, String
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class ProgrammingLanguage(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'programming_languages'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    about = Column(String, nullable=False)
    href = Column(String, nullable=False)

    def __repr__(self):
        return f'<ProgrammingLanguage> {self.id} {self.name}'