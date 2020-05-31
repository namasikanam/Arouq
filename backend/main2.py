from flask import *
from flask_api import status
from correct import correct

app = Flask(__name__)
@app.route('/correct', methods = ['GET'])
def correct():
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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8002', debug = True)