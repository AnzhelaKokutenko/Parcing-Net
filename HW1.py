import requests
import json
from pprint import pprint
user = 'AnzhelaKokutenko'
url = f"https://api.github.com/users/{user}/repos"
response = requests.get(url).json()

pprint(response)

list = []
for i in response:
    list.append(i['name'])
print(f'Список репозиториев пользователя {user}{list}')

with open('file.json', 'w') as f:
    json.dump(response, f)

