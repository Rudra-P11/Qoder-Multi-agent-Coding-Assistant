import requests

response = requests.get('https://api.restful-api.dev/objects')
items = response.json()

for item in items:
    print(item)
