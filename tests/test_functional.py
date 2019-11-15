import urllib.request
import json
import os


ADDR = f'http://{os.environ["APP_ADDR"]}:5000'
RESULT_ID = ''


def make_request(addr):
    with urllib.request.urlopen(addr) as url:
        return json.loads(url.read().decode('utf-8'))


def test_index_page():
    response = make_request(ADDR)
    assert 'status' in response
    assert 'message' in response
    assert 'result' in response
    assert 'host_name' in response


def test_index_page_content():
    response = make_request(ADDR)
    assert response['status'] == 0
    assert response['message'] == 'Done.'
    assert response['result'] == ['Index.']


def test_notes_page():
    response = make_request(f'{ADDR}/notes')
    assert 'status' in response
    assert 'message' in response
    assert 'result' in response
    assert 'host_name' in response


def test_notes_page_content():
    response = make_request(f'{ADDR}/notes')
    assert response['status'] == 0
    assert response['message'] == 'Done.'
    assert type(response['result']) == list


def test_note_page():
    response = make_request(f'{ADDR}/note')
    assert response['status'] == 1
    assert response['message'] == 'Bad request. Method not allowed.'
    assert response['result'] == []


def test_note_empty_result():
    response = make_request(f'{ADDR}/note/lkajsdf823')
    assert response['status'] == 0
    assert response['message'] == 'Done.'
    assert response['result'] == {}


def test_wrong_address():
    response = make_request(f'{ADDR}/bones/uriel')
    assert response['status'] == 1
    assert response['message'] == 'Bad request. Address not found.'
    assert response['result'] == []


def test_create_note():
    header = {'Content-Type': 'application/json'}
    data = {'note': 'Greed is good.', 'user_name': 'Sorlag'}
    bdata = json.dumps(data).encode('utf-8')
    req = urllib.request.Request(f'{ADDR}/note', method='POST',
                                 data=bdata, headers=header)
    with urllib.request.urlopen(req) as response:
        res = json.loads(response.read())
    assert res['status'] == 0
    assert res['message'] == 'Done.'
    assert res['result']['note'] == data['note']
    assert res['result']['user_name'] == data['user_name']
    global RESULT_ID
    # bad practice, I know it.
    RESULT_ID = res['result']['id']


def test_get_note():
    res = make_request(f'{ADDR}/note/{RESULT_ID}')
    assert res['status'] == 0
    assert res['message'] == 'Done.'
    assert res['result']['note'] == 'Greed is good.'
    assert res['result']['user_name'] == 'Sorlag'
    assert res['result']['id'] == RESULT_ID
