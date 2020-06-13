# Text Processing Python REST API Server 

![REST Server](https://github.com/Sumaid/keyword_server/workflows/Python%20package/badge.svg?branch=master)
Deployed : https://lemmatizer-api.herokuapp.com/

## Project layout

        wsgi.py      # Flask application container
        requirements.txt    # Python libraries requirements
        Procfile        # Heroku deployment instructions
        nltk.txt        # NLTK modules required
        en_core_web_sm-2.2.0.tar.gz    # Embeddings for text processing
        .gitignore        # Ignore files in version control
        averaged_perceptron    # Wordnet embeddings required for text processing
        tests/          # Unit Tests corresponding to different APIs
        app/
            main.py     # Server Main Logic
            templates/
                index.html    # Root page of server



## APIs

### Keywords retrieval
    Get keywords including phrases from text corpus
    /getKeywords/ (GET method)		
    Example : https://lemmatizer-api.herokuapp.com/getKeywords/Life is a matter of good choices and bad choices.

### Lemmatization
    Get lemmas of words which are passed as comma seperated string
    /getLemmas/ (GET method)		
    Example : https://lemmatizer-api.herokuapp.com/getLemmas/loved,rocks,love

### Tokenization, Stop words removal, lemmatization
    Tokenize, Remove stop words, Lemmatize the corpus	
    /transformCorpus/ (GET method)	
    Example : https://lemmatizer-api.herokuapp.com/transformCorpus/(This is a string)

### Add & Remove filter words
    Adding filter words	
    /addFilterWords/ (POST method)	
    Example: curl -H "Content-Type: application/json" -X POST -d '{"words":["love"]}' https://lemmatizer-api.herokuapp.com/addFilterWords/

    Remove filter words	
    /removeFilterWords/ (POST method)	
    Example : curl -H "Content-Type: application/json" -X POST -d '{"words":["love"]}' https://lemmatizer-api.herokuapp.com/removeFilterWords/

        