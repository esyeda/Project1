import requests
import os
from dotenv import load_dotenv

load_dotenv()

trip_api_key = os.getenv('TRIP_API_KEY')
genai_key = os.getenv('GENAI_KEY')

url = "https://api.content.tripadvisor.com/api/v1/location/search?language=en"
headers = {"accept": "application/json"}
response = requests.get(url, headers=headers)
