from app.main import app
from urllib.parse import urlencode
import json

def test_transformcorpus():
    res = app.test_client().get('/transformCorpus/(This is a string)')
    result = json.loads(res.data.decode('utf-8'))
    assert result['words'] == ["string"]