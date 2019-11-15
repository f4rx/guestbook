# -*- coding: utf-8 -*-
"""
The module that runs the program.
"""
from guest_book import app
import bjoern

bjoern.run(app, host=app.config["APP_ADDRESS"], port=int(app.config["APP_PORT"]))