# -*- coding: utf-8 -*-
"""This module contains a class that defines the basic configurations of a web
service.
"""
import os

class Config(object):
    """This class defines the basic configurations of a web service.
    """
    DB_USER = os.environ.get('MYSQL_USER', 'root')
    DB_PASSWORD = os.environ.get('MYSQL_PASSWORD', 'Celestial352')
    DB_ADDRESS = os.environ.get('MYSQL_SERVER_ADDRESS', '127.0.0.1')
    DB_NAME = os.environ.get('MYSQL_DATABASE', 'guest_book')
    APP_PORT = os.environ.get('GUESTBOOKAPP_PORT', 5000)
    APP_ADDRESS = os.environ.get('APP_ADDRESS', '127.0.0.1')
