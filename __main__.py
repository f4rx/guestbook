# -*- coding: utf-8 -*-
"""
The module that runs the program.
"""
import time
import sys
import sqlalchemy.exc
CONNECTION_TRY_LIMIT = 7
CONNECTION_RETRY_TIME_LIMIT = 5
while True:
    try:
        from guest_book import app
        break
    except sqlalchemy.exc.OperationalError as error:
        if not CONNECTION_TRY_LIMIT:
            print(error)
            sys.exit(1)
        print('Waiting for connection...')
        CONNECTION_TRY_LIMIT -= 1
        time.sleep(CONNECTION_RETRY_TIME_LIMIT)
import bjoern

bjoern.run(app, host=app.config["APP_ADDRESS"], port=int(app.config["APP_PORT"]))