from flask_restful import abort, Resource
from flask import jsonify
from data import db_session
from data.users import User
from data.olympiads import Olympiad
from data.programming_languages import ProgrammingLanguage


def abort_if_user_not_found(email):
    session = db_session.create_session()
    news = session.query(User).get(email)
    if not news:
        abort(404, message=f"User {email} not found")


class ApiUser(Resource):
    def get(self, email):
        session = db_session.create_session()
        user = session.query(User).filter(User.email == email).first()
        if not user:
            abort(404, message=f"User {email} not found")
        return jsonify({email: user.to_dict(only=('name', 'about', 'created_date', 'admin'))})


class ApiProgrammingLanguage(Resource):
    def get(self, name):
        session = db_session.create_session()
        language = session.query(ProgrammingLanguage).filter(ProgrammingLanguage.name == name).first()
        if not language:
            abort(404, message=f"ProgrammingLanguages {name} not found")
        return jsonify({name: language.to_dict(only=('about', 'href'))})


class ApiOlympiads(Resource):
    def get(self, type_olympiad):
        session = db_session.create_session()
        olympiads = session.query(Olympiad).filter(Olympiad.type == type_olympiad.capitalize()).all()
        if not olympiads:
            abort(404, message=f"Olympiads {type_olympiad} not found")
        return jsonify({type_olympiad: [item.to_dict(
            only=('date', 'href')) for item in olympiads]})