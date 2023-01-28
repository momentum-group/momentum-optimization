from solve import scheduling
from flask import Flask, jsonify, request
from pulp import *

app = Flask(__name__)

@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.get_json()
    people = data['people']
    max_hours = data['max_hours']
    min_hours = data['min_hours']
    preferred_hours = data['preferred_hours']
    needed_capacity = data['needed_capacity']
    
    x = scheduling(people, max_hours, min_hours, preferred_hours, needed_capacity)

    return jsonify({'result': x})


if __name__ == '__main__':
    app.run()