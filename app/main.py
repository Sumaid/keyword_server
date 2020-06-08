from nltk.corpus import wordnet as wn
from flask import Flask, jsonify
from nltk import pos_tag
from collections import defaultdict
import nltk
nltk.download('wordnet')
nltk.download('averaged_perceptron_tagger')
lemmatizer = nltk.stem.WordNetLemmatizer()
tag_map = defaultdict(lambda : wn.NOUN)
tag_map['J'] = wn.ADJ
tag_map['V'] = wn.VERB
tag_map['R'] = wn.ADV

app = Flask(__name__) 
  
@app.route("/") 
def home_view(): 
        return "<h2>Go to /getLemmas/wordList, wordList is a string with comma seperated words </h2>"

@app.route("/getLemmas/<wordList>", methods=['GET']) 
def get_lemmas(wordList):
        return jsonify([lemmatizer.lemmatize(token, tag_map[tag[0]]) for token, tag in pos_tag(wordList.split(','))])

@app.route("/getLemmas/", methods=['GET']) 
def get_lemmas_nowords():
        return jsonify([])
