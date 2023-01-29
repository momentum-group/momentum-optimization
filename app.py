from solve import scheduling
from flask import Flask, jsonify, request
from pulp import *

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def hello_world():
    return 'Just Updated'

@app.route('/send_back', methods=['POST', 'GET'])
def send_back():
    data = request.get_json()
    return jsonify(data)


@app.route('/schedule', methods=['POST'])
def schedule():
    data = json.loads(request.data)

    people = data['people']
    max_hours = data['max_hours']
    min_hours = data['min_hours']
    preferred_hours = data['preferred_hours']
    needed_capacity = data['needed_capacity']
    
    try:
        print(people, max_hours, min_hours, preferred_hours, needed_capacity)
        prob, x = scheduling(people, max_hours, min_hours, preferred_hours, needed_capacity)
    except Exception as e:
        # return jsonify({'status': f'error: {e}'})
        prob, x = scheduling(people, max_hours, min_hours, preferred_hours, needed_capacity)

    return jsonify({'result': x, 'status': LpStatus[prob.status], 'objective': value(prob.objective)})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)