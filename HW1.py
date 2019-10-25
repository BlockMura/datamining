# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев
# для конкретного пользователя, сохранить JSON-вывод в файле *.json.**

import requests
import json
from datetime import datetime as dt



from requests import Response

url = 'https://api.github.com/users/BlockMura/repos'

result_repo = []

data = requests.get(url)
j_data = data.json()

result_repo.extend(data.json())
print(result_repo)

with open (f'result_repo_{int(dt.now().timestamp())}.json', 'w') as j_file:
    j_file.write(json.dumps(result_repo))

#2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import json
import vk

session = vk.Session(access_token='{7171520}')

api = vk.API(session)

client_id = "<7171520>"
client_secret = "<yjb6YJdph1l25ai4RL0P>"
authorization_base_url = 'https://oauth.vk.com/authorize?'
token_url = 'https://oauth.vk.com/blank.html#access_token'

#к сожалению только сегодня начал делать дз поэтому нет времени