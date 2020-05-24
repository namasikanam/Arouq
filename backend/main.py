from flask import *
from flask_api import status
from utils import contain_english
from bert_qa import bert_QA as english_qa
from xlore_qa import xlore_QA as chinese_qa

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/QA', methods = ['GET'])
def QA():
    print(request.args)
    question = request.args.get('question')
    print("[Router] Question: {}".format(question))
    if contain_english(question):
        ans, score = english_qa(question)
        if score < 3:
            ans = None
    else:
        ans = chinese_qa(question)
    if ans is not None:
        return jsonify({
            'msg': 'Success',
            'answer': ans
        })
    else:
        return jsonify({
            'msg': 'NoAnswer',
        })

if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5001', debug = True)