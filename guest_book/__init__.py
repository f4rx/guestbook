# -*- coding: utf-8 -*-
"""
Init module.
"""
import socket
import flask
from guest_book import config


app = flask.Flask(__name__)
app.config.from_object(config.Config)


def get_cur_addr() -> str:
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.connect(('10.255.255.255', 1))
        addr = sock.getsockname()[0]
    except:
        addr = '127.0.0.1'
    sock.close()
    return addr


CUR_ADDR = get_cur_addr()

from guest_book import routes

