import requests
r = requests.get('http://127.0.0.1:5000/users')
r = requests.post('http://127.0.0.1:5000/users', json={"id": 1, "name": "Peter", "surname": "Jan"})
print(r.json())
r = requests.delete('http://127.0.0.1:5000/users', json={"id": 100})
print(r.json())
r = requests.put('http://127.0.0.1:5000/users', json={"id": 8, "name": "Nikita", "surname": "Filatov"} )
print(r.json())
r = requests.put('http://127.0.0.1:5000/users', json={"id": 1, "name": "New", "surname": "York"})
