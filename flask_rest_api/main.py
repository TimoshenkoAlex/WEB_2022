import json
from flask import Flask, jsonify, request
app = Flask(__name__)
data = [{'id': 0, 'name': 'Alex', 'surname': 'Turner'},
        {'id': 1, 'name': 'Tom', 'surname': 'York'},
        {'id': 2, 'name': 'Kek', 'surname': 'Mem'},
        {'id': 3, 'name': 'Konstnatin', 'surname': 'Voronin'}]


@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(data)


@app.route('/users', methods=['POST'])
def add_user():
    for i in range(len(data)):
        if request.get_json()['id'] == data[i]['id']:
            print('id уже существует')
            break
    else:
        data.append(request.get_json())
    return jsonify(data)


@app.route('/users', methods=['DELETE'])
def del_user():
    if request.get_json()['id'] in [data[i]['id'] for i in range(len(data))]:
        data.pop([i for i, x in enumerate(data) if x['id'] == request.get_json()['id']][0])
    else:
        print('Такого id не существует')
    return jsonify(data)


@app.route('/users', methods=['PUT'])
def update_user():
    if request.get_json()['id'] in [data[i]['id'] for i in range(len(data))]:
        data[[i for i, x in enumerate(data) if x['id'] == request.get_json()['id']][0]] = request.get_json()
    else:
        print('Такого id не существует')
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)