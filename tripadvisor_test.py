import os
import requests

TRIPADVISOR_API_KEY = os.getenv('TRIPADVISOR_API_KEY')

'''print("API KEY:", TRIPADVISOR_API_KEY)
TRIPADVISOR_API_KEY = '6587D61217FA4ED8A4113B9511202EE7'''

url = "https://api.content.tripadvisor.com/api/v1/location/search?language=en"

cy = input("Enter the city that youre looking suggestions for: ")
cate = input("What are you looking for — a hotel, restaurant, or attraction? ")

data = {
    'key': TRIPADVISOR_API_KEY,
    'searchQuery': cy,
    'category': cate
}

response = requests.get(url, params=data)
print(response.status_code)
print(response.json())
