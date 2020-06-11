from nltk.corpus import wordnet as wn
from flask import request, Flask, jsonify, Response, render_template
from nltk import pos_tag
from nltk.corpus import stopwords
from collections import defaultdict
from textblob import TextBlob
import nltk
import json
lemmatizer = nltk.stem.WordNetLemmatizer()
stopwords_set = set(stopwords.words('english'))
stopwords_set.update(['a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'can', "can't", 'cannot', 'com', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'else', 'ever', 'few', 'for', 'from', 'further', 'get', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'http', 'I', "I'd", "I'll", "I'm", "I've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', 'just', 'k', "let's", 'like', 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor',
                      'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'r', 'same', 'shall', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'www', 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'])
tag_map = defaultdict(lambda: wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV

import spacy
import pytextrank
nlp = spacy.load("en_core_web_sm")
tr = pytextrank.TextRank()
nlp.add_pipe(tr.PipelineComponent, name="textrank", last=True)

app = Flask(__name__)


@app.route("/")
def home_view():
    return render_template("index.html", template_folder='templates')


@app.route("/getLemmas/<wordList>", methods=['GET'])
def get_lemmas(wordList):
    wordList = wordList.lower()
    return jsonify(words=[lemmatizer.lemmatize(token, tag_map[tag[0]]) for token, tag in pos_tag(wordList.split(','))])


@app.route("/getLemmas/", methods=['GET'])
def get_lemmas_nowords():
    return jsonify([])


@app.route("/transformCorpus/<word>", methods=['GET'])
def transpose_corpus(word):
    word = word.lower()
    filtered_words = [token for token in TextBlob(
        word).words if not token in stopwords_set and not token[0] == "'"]
    return jsonify(words=[lemmatizer.lemmatize(token, tag_map[tag[0]]) for token, tag in pos_tag(filtered_words)])


@app.route("/transformCorpus/", methods=['GET'])
def transpose_corpus_empty():
    return jsonify([])


@app.route("/addFilterWords/", methods=['POST'])
def transpose_corpus_add():
    try:
        stopwords_set.update([word.lower() for word in request.json['words']])
        return Response(status=200)
    except:
        return Response(status=400)


@app.route("/removeFilterWords/", methods=['POST'])
def transpose_corpus_remove():
    try:
        for word in request.json['words']:
            stopwords_set.discard(word)
            stopwords_set.discard(word.lower())
        return Response(status=200)
    except:
        return Response(status=400)


@app.route("/getKeywords/<word>", methods=['GET'])
def get_keyword(word):
    doc = nlp(word.lower())
    if len(doc._.phrases)>0:
        mx = doc._.phrases[0].rank
    else:
        mx = 1
    words = []
    for p in doc._.phrases:
        if p.rank>0:
            words += [{'phrase':p.text, 'rank':p.rank/mx}]
    return jsonify(words=words)


@app.route("/getKeywords/", methods=['GET'])
def get_keyword_empty():
    return jsonify(words=[])