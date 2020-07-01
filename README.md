# Text Processing Python REST API Server 

![REST Server](https://github.com/Sumaid/keyword_server/workflows/Python%20package/badge.svg?branch=master)

Deployed : https://lemmatizer-api.herokuapp.com/

## Project layout

        wsgi.py      # Flask application container
        requirements.txt    # Python libraries requirements
        Procfile        # Heroku deployment instructions
        en_core_web_sm-2.2.0.tar.gz    # Embeddings for text processing
        .gitignore        # Ignore files in version control
        tests/          # Unit Tests corresponding to different APIs
        app/
            main.py     # Server Main Logic
            templates/
                index.html    # Root page of server



## APIs

### Keywords retrieval
    Get keywords including phrases from text corpus
    /getKeywordsBatch/ (POST method)		
    Example : curl -H "Content-Type: application/json" -X POST -d '{"responses":["love is a drug", "i love excellent service"]}' http://lemmatizer-api.herokuapp.com/getKeywordsBatch/

## Local Development

### Install
    pip3 install -r requirements.txt

### Run
    python3 wsgi.py   # http://127.0.0.1:5000/

### Verify tests
    pytest
    pytest --cov=app tests/   # To check code coverage, prerequisite : pytest-cov pip package
