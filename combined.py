import os
import requests
from google import genai
from google.genai import types
from json_parsing import Parser
from dotenv import load_dotenv

# Set environment variables
load_dotenv()
TRIPADVISOR_API_KEY = os.getenv('TRIPADVISOR_API_KEY')
GENAI_KEY = os.getenv('GENAI_KEY')

# Create an genAI client
genai.api_key = GENAI_KEY
client = genai.Client(
    api_key=GENAI_KEY,
)

cy = input("Enter the city that youre looking suggestions for: ")
cate = input("What are you looking for — a hotel, restaurant, or attraction? ")

url = "https://api.content.tripadvisor.com/api/v1/location/search?language=en"
data = {
    'key': TRIPADVISOR_API_KEY,
    'searchQuery': cy,
    'category': cate
}

response = requests.get(url, params=data)
data_of_trip = response.json()

parser = Parser(data_of_trip)
parser.write_to_database(cate)

# Pull stored results
db_results = parser.pull_list(cate, cy)
for row in db_results:
    name = row._mapping.get('name')

    prompt = (
        f"{name} is a {cate} "
        f"in {cy}."
        "respond in two to three sentences why its good"
    )

    # Specify the model to use and the messages to send
    ai_response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=(
                "You are a helpful travel assistant."
            )
        ),
        contents=prompt,
    )

    print(ai_response.text)

    sugg = input("Want another suggestion? (Yes/No): ").lower().strip()
    if sugg != "yes":
        print("Enjoy!")
        break
