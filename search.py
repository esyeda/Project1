import requests

#Template taken directly from tripadvisor's documentation page, can't test it yet
url = "https://api.content.tripadvisor.com/api/v1/location/search?language=en"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)