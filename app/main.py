from flask import request, Flask, jsonify, Response, render_template
import spacy
import pytextrank
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

nlp = spacy.load("en_core_web_sm")
tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)
app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()


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
        for sentence in request.json['responses']:
            if not sentence: return jsonify(words=[[]])
            try:
                doc = nlp(sentence.lower())
                if len(doc._.phrases)>0:
                    max_rank = doc._.phrases[0].rank    # phrases are recieved in decreasing order of their rank, so first phrase rank is highest
                else:
                    max_rank = 1
                if max_rank == 0:                       # max_rank shouldn't be 0 to avoid division by 0 exception
                    max_rank = 1
                result += [[{'phrase':p.text, 'rank':p.rank/max_rank, 'count':p.count} for p in doc._.phrases]]
            except Exception as e:
                print('Response is : ', sentence)
                print('Response processing Error : ',e)
                return Response(400)
        return jsonify(words=result)
    except Exception as e: 
        print('getKeywordsBatch Error : ',e)
        return Response(400)

@app.route("/getKeywordsWithSentiment/", methods=['POST'])
def get_keywords_sentiment():
    """
    API to get keywords and phrases with their rank & sentiments
    Input : text corpus
    Output : list of words and phrases with their rank/frequency & list of sentiments(-1 to 1) of each response
    """
    try:
        result = []
        sentiments = []
        if len(request.json['responses']) == 0: return jsonify(words=[[]], sentiments=[])
        for sentence in request.json['responses']:
            if not sentence: return jsonify(words=[[]], sentiments=[])
            try:
                doc = nlp(sentence.lower())
                if len(doc._.phrases)>0:
                    max_rank = doc._.phrases[0].rank   # phrases are recieved in decreasing order of their rank, so first phrase rank is highest
                else:
                    max_rank = 1
                if max_rank == 0:                      # max_rank shouldn't be 0 to avoid division by 0 exception
                    max_rank = 1
                result += [[{'phrase':p.text, 'rank':p.rank/max_rank, 'count':p.count} for p in doc._.phrases]]
                sentiments += [analyzer.polarity_scores(sentence)['compound']]
            except Exception as e:
                print('Response is : ', sentence)
                print('Response processing Error : ',e)
                return Response(400)
        return jsonify(words=result, sentiments=sentiments)
    except Exception as e: 
        print('getKeywordsWithSentiment Error : ',e)
        return Response(400)