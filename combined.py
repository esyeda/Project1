#trip advisor 
import os
import requests
from google import genai
from google.genai import types

# Set environment variables
TRIPADVISOR_API_KEY = os.getenv('TRIPADVISOR_API_KEY')
GENAI_KEY = os.getenv('GENAI_KEY')

# Create an genAI client using the key from our environment variable
genai.api_key = GENAI_KEY
client = genai.Client(
    api_key=my_api_key,
)

url = "https://api.content.tripadvisor.com/api/v1/location/search?language=en"
data = {
    'key': TRIPADVISOR_API_KEY,
    'searchQuery': cy,
    'category': cate
}

cy = input("Enter the city that youre looking suggestions for: ")
cate = input("What are you looking for — a hotel, restaurant, or attraction? ")

response = requests.get(url, params=data)
print(response.status_code)
print(response.json())

#gen ai 

# Create an genAI client using the key from our environment variable
client = genai.Client(
    api_key=my_api_key,
)

# AI Prompt
prompt = (
    f"recommend the top {cate} "
    f"in {cy} and explain why it's better."
)

# Specify the model to use and the messages to send
response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        system_instruction=(
            "You are a nice travel assistant who gives helpful suggestions."
        )
    ),
    contents=prompt,
)

print(response.text)
