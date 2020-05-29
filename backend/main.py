from flask import *
from flask_api import status
from utils import contain_english
from bert_qa import bert_QA as english_qa
from xlore_qa import xlore_QA as chinese_qa
from correct import correct

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def QA():
    print(request.args)
    query = request.args.get('query')
    print("[Router] Query: {}".format(query))
    if contain_english(query):
        ans, score = english_qa(query)
        if score < 3:
            ans = None
    else:
        ans = chinese_qa(query)
    if ans is None:
        ans = ''

    corrected = correct(query)
    if corrected is None:
        corrected = ''

    return jsonify({
        'answer': ans,
        'corrected': corrected,
        'total': 0,
        'documents': []
    })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='8001', debug = True)
