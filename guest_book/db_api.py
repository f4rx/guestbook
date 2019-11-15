# -*- coding: utf-8 -*-
"""
This module contains the functionality of accessing the database.
"""
import os
import time
import json
import sqlalchemy
import uuid
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import String, Column, DateTime, Unicode
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from guest_book import config, app, CUR_ADDR


Base = declarative_base()
conn_string = (f'mysql+pymysql://'
               f'{app.config["DB_USER"]}:'
               f'{app.config["DB_PASSWORD"]}@'
               f'{app.config["DB_ADDRESS"]}/'
               f'{app.config["DB_NAME"]}'
               f'?charset=utf8')
engine = sqlalchemy.create_engine(conn_string, echo=True)
if not database_exists(engine.url):
    create_database(engine.url)
Session = sessionmaker(bind=engine)


class WebServiceError(Exception):
    pass


class Notes(Base):

    __tablename__ = 'notes'
    id = Column(String(36), primary_key=True, auto_increment=False)
    user_name = Column(Unicode(64, collation='utf8_bin'))
    note = Column(Unicode(256, collation='utf8_bin'))
    date_time = Column(DateTime)
    server_name = Column(String(64))

    def __repr__(self) -> str:
        return (f'Note(id={self.id}, user_name={self.user_name},'
                f'note={self.note}, date_time={self.date_time},'
                f'server_name={self.server_name})')

    @property
    def dict(self) -> dict:
        return {'id': self.id, 'user_name': self.user_name, 'note': self.note,
                'date_time': self.date_time.strftime('%H:%M:%S %d-%m-%Y'),
                'server_name': self.server_name}


def get_notes() -> list:
    session = Session()
    res = session.query(Notes).order_by(Notes.date_time).all()
    return [r.dict for r in res]


def get_note(note_id: str) -> dict:
    session = Session()
    res = session.query(Notes).filter(Notes.id == note_id).all()
    res = [r.dict for r in res]
    return res[0] if res else {}


def create_note(request_body: str) -> dict:
    try:
        body = json.loads(request_body)
    except (TypeError, json.decoder.JSONDecodeError):
        msg = ('Cannot serialize request body. The request body must be at '
               'json format.')
        raise WebServiceError(msg)
    note_id = str(uuid.uuid4()).replace('-', '')
    rec = Notes(user_name=body['user_name'], server_name=CUR_ADDR,
                date_time=time.localtime(), note=body['note'],
                id=note_id)
    session = Session()
    session.add(rec)
    session.commit()
    res = session.query(Notes).filter(Notes.id == note_id).all()
    res = [r.dict for r in res]
    return res[0] if res else {}


Base.metadata.create_all(engine)
