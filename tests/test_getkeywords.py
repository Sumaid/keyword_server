from app.main import app
from urllib.parse import urlencode
import json

def test_getkeywords():
    res = app.test_client().get('/getKeywords/Life is a matter of good choices')
    result = json.loads(res.data.decode('utf-8'))
    assert len(result['words']) == 3
    assert result['words'][0]['phrase'] == "good choices"
    assert result['words'][1]['phrase'] == "life"
    assert result['words'][2]['phrase'] == "a matter"