# -*- coding: utf-8 -*-
"""
Init module.
"""
import flask
from guest_book import config

app = flask.Flask(__name__)
app.config.from_object(config.Config)

from guest_book import routes

