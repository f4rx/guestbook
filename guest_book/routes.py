# -*- coding: utf-8 -*-
"""
This module implements the definition of web service routes.
"""
import os
import json
from flask import request, Response
import werkzeug.exceptions
from guest_book import app, db_api, CUR_ADDR


@app.route('/', methods=['GET'])
@app.route('/index')
def index() -> Response:
    resp = dict(status=0, message='Done.', result=['Index.'],
                host_name=CUR_ADDR)
    return Response(json.dumps(resp), content_type='application/json',
                    mimetype='application/json')


@app.route('/notes', methods=['GET'])
def get_notes() -> Response:
    resp = dict(status=0, message='Done.', result=[],
                host_name=CUR_ADDR)
    res = db_api.get_notes()
    resp['result'] = res
    return Response(json.dumps(resp), content_type='application/json',
                    mimetype='application/json')


@app.route('/note/<string:note_id>', methods=['GET'])
def get_note(note_id: str) -> Response:
    resp = dict(status=0, message='Done.', result=[],
                host_name=CUR_ADDR)
    res = db_api.get_note(note_id)
    resp['result'] = res
    return Response(json.dumps(resp), content_type='application/json',
                    mimetype='application/json')


@app.route('/note', methods=['POST'])
def create_note() -> Response:
    resp = dict(status=0, message='Done.', result=[],
                host_name=CUR_ADDR)
    body = request.data.decode('utf-8').strip()
    try:
        res = db_api.create_note(body)
    except db_api.WebServiceError as error:
        resp['status'] = 1
        resp['message'] = str(error)
        resp['result'] = []
        return Response(json.dumps(resp), content_type='application/json',
                        mimetype='application/json')
    resp['result'] = res
    return Response(json.dumps(resp), content_type='application/json',
                    mimetype='application/json')


@app.errorhandler(404)
def not_found(error: werkzeug.exceptions.NotFound) -> Response:
    resp = dict(status=1, message='Bad request. Address not found.', result=[],
                host_name=CUR_ADDR)
    return Response(json.dumps(resp), content_type='application/json',
                    mimetype='application/json')


@app.errorhandler(405)
def not_allowed(error: werkzeug.exceptions.MethodNotAllowed) -> Response:
    resp = dict(status=1, message='Bad request. Method not allowed.', result=[],
                host_name=CUR_ADDR)
    return Response(json.dumps(resp), content_type='application/json',
                    mimetype='application/json')
