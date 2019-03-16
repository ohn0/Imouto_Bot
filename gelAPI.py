import requests

apicall = "https://gelbooru.com/index.php?page=dapi&s=post&q=index&limit=10&json=1&tags=ahegao"

response = requests.get(apicall)
response = response.json()

print(response)

for r in response:
    print(r['file_url'])




