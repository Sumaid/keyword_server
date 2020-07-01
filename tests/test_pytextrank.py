from .context import app
from urllib.parse import urlencode
import json
import pytest

def test_root():
    from app.main import app
    res = app.test_client().get('/')
    assert res

def test_pytextrank():

    from app.main import app
    datastring = {
        "responses" : ["Life is good"]
        }
    res = app.test_client().post('/getKeywordsBatch/', json=datastring)
    result = json.loads(res.data.decode('utf-8'))
    assert len(result['words']) == 1
    assert result['words'][0][0]['phrase'] == "life"
    assert result['words'][0][0]['count'] == 1
    assert result['words'][0][0]['rank'] == 1.0

def test_pytextrank_empty():

    from app.main import app
    datastring = {
        "responses" : []
        }
    res = app.test_client().post('/getKeywordsBatch/', json=datastring)
    result = json.loads(res.data.decode('utf-8'))
    assert result['words'] == [[]]

def test_pytextrank_empty_phrases():

    from app.main import app
    datastring = {
        "responses" : ["the"]
        }
    res = app.test_client().post('/getKeywordsBatch/', json=datastring)
    result = json.loads(res.data.decode('utf-8'))
    assert result['words'] == [[]]

def test_pytextrank_empty_response():

    from app.main import app
    datastring = {
        "responses" : [""]
        }
    res = app.test_client().post('/getKeywordsBatch/', json=datastring)
    result = json.loads(res.data.decode('utf-8'))
    assert result['words'] == [[]]

def test_pytextrank_exception_response():

    from app.main import app
    datastring = {
        "words" : [""]
        }
    with pytest.raises(Exception):
        res = app.test_client().post('/getKeywordsBatch/', json=datastring)
        result = json.loads(res.data.decode('utf-8'))
        assert result['words'] == [[]]