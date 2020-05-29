from flask import *
from flask_api import status
from utils import contain_english
from bert_qa import bert_QA as english_qa
from xlore import run as chinese
from correct import correct

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def QA():
    print(request.args)
    query = request.args.get('query')
    print("[Router] Query: {}".format(query))
    related = []
    if contain_english(query):
        ans, score = english_qa(query)
        if score < 3:
            ans = None
    else:
        ret = chinese(query)
        ans = ret['QA_ret']
        related = ret['related']
    if ans is None:
        ans = ''

    corrected = correct(query)
    if corrected is None:
        corrected = ''

    result = {
        'answer': ans,
        'corrected': corrected,
        'total': 0,
        'related': related,
        'documents': []
    }
    print(result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8001', debug = True)
