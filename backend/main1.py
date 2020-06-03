from flask import *
from flask_api import status
from utils import contain_english
from bert_qa import bert_QA as english_qa
from xlore import run as chinese
from auto_fill import auto_fill
from xlore import solr

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def main_query():
    print(request.args)
    query = request.args.get('query')
    page = int(request.args.get('page'))

    print("[Router] Query: {}".format(query))
    
    ans = None
    keyword = None
    if contain_english(query):
        if page == 1:
            ans, score, keyword = english_qa(query)
            if score < 3:
                ans = None
                keyword = None
        related = []
    else:
        ret = chinese(query)
        if page == 1:
            ans = ret['QA_ret']
        related = ret['related']
        keyword = ret['keyword']
    total, documents = solr(query, page, keyword)

    result = {
        'answer': ans if ans is not None else '',
        'total': total,
        'related': related,
        'documents': documents
    }
    print(result)
    return jsonify(result)


@app.route('/en/', methods = ['GET'])
def en_query():
    print(request.args)
    query = request.args.get('query')
    page = int(request.args.get('page'))

    print("[Router] English Query: {}".format(query))
    
    ans = None
    keyword = None
    if page == 1:
        ans, score, keyword = english_qa(query)
        if score < 3:
            ans = None
            keyword = None
    total, documents = solr(query, page, keyword)

    result = {
        'answer': ans if ans is not None else '',
        'total': total,
        'related': [],
        'documents': documents
    }
    return jsonify(result)

@app.route('/zh/', methods = ['GET'])
def zh_query():
    print(request.args)
    query = request.args.get('query')
    page = int(request.args.get('page'))

    print("[Router] Chinese Query: {}".format(query))
    
    ans = None
    keyword = None
    ret = chinese(query)
    if page == 1:
        ans = ret['QA_ret']
    related = ret['related']
    keyword = ret['keyword']
    total, documents = solr(query, page, keyword)

    result = {
        'answer': ans if ans is not None else '',
        'total': total,
        'related': related,
        'documents': documents
    }
    return jsonify(result)


@app.route('/fill/', methods = ['GET'])
def fill():
    print(request.args)
    word = request.args.get('query')
    print("[Router] fill: {}".format(word))
    result = {
        'candidates': auto_fill(word),
    }
    print(result)
    return jsonify(result)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8001', debug = True)
