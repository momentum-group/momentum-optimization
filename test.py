import requests
import json

people = [[0, 0, 1, 1, 1, 1, 1, 1, 1, 1],
          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

max_hours = [5, 4]
min_hours = [1, 1]
preferred_hours = [4, 4]
needed_capacity = [1, 1, 1, 2, 2, 2, 2, 1, 1, 0]

data = {
    'people': people,
    'max_hours': max_hours,
    'min_hours': min_hours,
    'preferred_hours': preferred_hours,
    'needed_capacity': needed_capacity
}

# send post to localhost:5000/schedule 104.248.109.231
r = requests.post('http://104.248.109.231:5000/schedule', data=json.dumps(data))

# if not an error, print the response
print(r.json())
