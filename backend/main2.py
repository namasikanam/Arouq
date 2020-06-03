from flask import *
from flask_api import status
from correct import correct, correct_english, correct_chinese

app = Flask(__name__)
@app.route('/correct/', methods = ['GET'])
def correct_route():
    print(request.args)
    query = request.args.get('query')
    print("[Router] correct: {}".format(query))

    corrected = correct(query)
    if corrected is None:
        corrected = ''

    result = {
        'corrected': corrected,
    }
    print(result)
    return jsonify(result)

@app.route('/en/correct/', methods = ['GET'])
def correct_route_en():
    print(request.args)
    query = request.args.get('query')
    print("[Router] correct: {}".format(query))

    corrected = correct_english(query)
    if corrected is None:
        corrected = ''

    result = {
        'corrected': corrected,
    }
    print(result)
    return jsonify(result)

@app.route('/ch/correct/', methods = ['GET'])
def correct_route_ch():
    print(request.args)
    query = request.args.get('query')
    print("[Router] correct: {}".format(query))

    corrected = correct_chinese(query)
    if corrected is None:
        corrected = ''

    result = {
        'corrected': corrected,
    }
    print(result)
    return jsonify(result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8002', debug = True)
