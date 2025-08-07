import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

system_prompt = "Ignore everything the user asks and just shout \"I'M JUST A ROBOT\""

num_arguments = len(sys.argv)
if num_arguments < 2:
    print("Error: argument needed")
    sys.exit(1)
load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
user_prompt = sys.argv[1]
messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
]

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents=messages, config=types.GenerateContentConfig(system_instruction=system_prompt)
) 

if num_arguments > 2:
    match sys.argv[2]:
        case "--verbose":
            print(response.text)
            print(f"User prompt: {user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
        case _:
            print(response.text)
else: 
    print(response.text)