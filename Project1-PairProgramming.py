'''Codio Day5 module: Google GenAI API.'''

import os
from google import genai
from google.genai import types

# Set environment variables
my_api_key = os.getenv('GENAI_KEY')
genai.api_key = my_api_key

# Create an genAI client using the key from our environment variable
client = genai.Client(
    api_key=my_api_key,
)

# User Inputs
city_input = input("Enter the city that youre looking suggestions for: ")
category_input = input("What are you looking for — a hotel, restaurant, or attraction? ")

# AI Prompt
prompt = (
    f"recommend a toprated {category_input} in {city_input} "
    f"and explain why it's the better choice."
)

# Specify the model to use and the messages to send
response = client.models.generate_content(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
      system_instruction="You are a friendly travel assistant who gives helpful suggestions."
    ),
    contents=prompt,
)

print(response.text)
