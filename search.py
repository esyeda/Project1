import requests

url = "https://api.content.tripadvisor.com/api/v1/location/search?language=en"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)
