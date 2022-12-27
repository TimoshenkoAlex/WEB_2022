import json
from flask import Flask, jsonify, request, render_template
import psycopg2
import random
from operator import itemgetter
app = Flask(__name__)
users = []
conn = psycopg2.connect(
    host='localhost',
    database='Web2022',
    user='postgres',
    password='12345'
)
cursor = conn.cursor()

sucess_message = {'sucess': True}

id_error = {"error": "Пользователя с таким id не существует в базе данных, проверьте вводимые данные"}

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.route('/users', methods=['GET'])
def get_users():
    users.clear()
    sql = 'select * from users'
    cursor.execute(sql)
    data = cursor.fetchall()
    for el in data:
        user = {'id': el[0], 'name': el[1], 'surname': el[2]}
        users.append(user)
    sorted_users = sorted(users, key=itemgetter('id'))
    return jsonify(sorted_users)


@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    get_users()
    if id in [users[i]['id'] for i in range(len(users))]:
        sql = 'select * from users where id = %s'
        cursor.execute(sql, (int(id),))
        data = cursor.fetchall()
        user = {'id': data[0][0], 'name': data[0][1], 'surname': data[0][2]}
        return jsonify(user)
    else:
        print('Такого id не существует')
        return "Такого id не существует"


@app.route('/users', methods=['POST'])
def add_user():
    get_users()
    sql = 'INSERT INTO users VALUES (%s, %s, %s);'
    if request.get_json()['id'] in [users[i]['id'] for i in range(len(users))]:
        print('Такой id уже существует')
    else:
        id = request.json['id']
        name = request.json['name']
        surname = request.json['surname']
        cursor.execute(sql, (id, name, surname))
        conn.commit()
    return jsonify(sucess_message)


@app.route('/users', methods=['DELETE'])
def del_user():
    get_users()
    sql = 'DELETE FROM users WHERE id = %s;'
    if request.get_json()['id'] in [users[i]['id'] for i in range(len(users))]:
        id = request.get_json()['id']
        cursor.execute(sql, (int(id),))
        conn.commit()
        get_users()
        return get_users()
    else:
        print('Такого id не существует')
        return jsonify(id_error)


@app.route('/users', methods=['PUT'])
def update_user():
    get_users()
    if request.get_json()['id'] in [users[i]['id'] for i in range(len(users))]:
        sql = 'UPDATE public.users SET name=%s, surname=%s WHERE id = %s;'
        id = request.json['id']
        name = request.json['name']
        surname = request.json['surname']
        cursor.execute(sql, (name, surname, int(id)))
        conn.commit()
        return get_users()
    else:
        print('Такого id не существует')
        return jsonify(id_error)


if __name__ == '__main__':
    app.run(debug=True)