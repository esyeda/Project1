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
cy = input("Enter the city that youre looking suggestions for: ")
cate = input("What are you looking for — a hotel, restaurant, or attraction? ")

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
