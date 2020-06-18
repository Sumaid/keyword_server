from flask import request, Flask, jsonify, Response, render_template
import json
from collections import defaultdict
import spacy
import pytextrank


nlp = spacy.load("en_core_web_sm")
tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)
app = Flask(__name__)


@app.route("/")
def home_view():
    """
    Home/Default page of server, returns a HTML with list of APIs and their purposes
    """
    return render_template("index.html", template_folder='templates')

@app.route("/getKeywordsBatch/", methods=['POST'])
def get_keywords_batch():
    """
    API to get keywords and phrases with their rank using pytextrank library
    Input : text corpus
    Output : list of words and phrases with their rank/frequency
    """
    try:
        result = []
        if len(request.json['responses']) == 0: return jsonify(words=[[]])
        for word in request.json['responses']:
            if not word: return jsonify(words=[])
            doc = nlp(word.lower())
            if len(doc._.phrases)>0:
                mx = doc._.phrases[0].rank
            else:
                mx = 1
            if mx == 0: mx = 1
            result += [[{'phrase':p.text, 'rank':p.rank/mx, 'count':p.count} for p in doc._.phrases]]
        return jsonify(words=result)
    except Exception as e: 
        print('getKeywordsBatch Error : ',e)
        return Response(400)
