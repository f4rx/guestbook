import urllib.request
import json


def make_request(addr):
    with urllib.request.urlopen(addr) as url:
        return json.loads(url.read().decode('utf-8'))


def test_index_page():
    response = make_request('http://10.50.2.10:5000/')
    assert 'status' in response
    assert 'message' in response
    assert 'result' in response
    assert 'host_name' in response


def test_index_page_content():
    response = make_request('http://10.50.2.10:5000/')
    assert response['status'] == 0
    assert response['message'] == 'Done.'
    assert response['result'] == ['Index.']


def test_notes_page():
    response = make_request('http://10.50.2.10:5000/notes')
    assert 'status' in response
    assert 'message' in response
    assert 'result' in response
    assert 'host_name' in response


def test_notes_page_content():
    response = make_request('http://10.50.2.10:5000/notes')
    assert response['status'] == 0
    assert response['message'] == 'Done.'
    assert type(response['result']) == list


def test_note_page():
    response = make_request('http://10.50.2.10:5000/note')
    assert response['status'] == 1
    assert response['message'] == 'Bad request. Method not allowed.'
    assert response['result'] == []


def test_note_empty_result():
    response = make_request('http://10.50.2.10:5000/note/lkajsdf823')
    assert response['status'] == 0
    assert response['message'] == 'Done.'
    assert response['result'] == {}


def test_wrong_address():
    response = make_request('http://10.50.2.10:5000/bones/uriel')
    assert response['status'] == 1
    assert response['message'] == 'Bad request. Address not found.'
    assert response['result'] == []
