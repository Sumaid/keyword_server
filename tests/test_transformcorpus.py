from .context import app
from urllib.parse import urlencode
import json
import nltk
mods = ['wordnet','averaged_perceptron_tagger','stopwords','punkt']
for mod in mods:
    nltk.download(mod)

def test_transformcorpus():
    from app.main import app
    res = app.test_client().get('/transformCorpus/(This is a string)')
    result = json.loads(res.data.decode('utf-8'))
    assert result['words'] == ["string"]