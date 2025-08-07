import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info,schema_get_files_info
from functions.get_file_content import get_file_content, schema_get_files_content
from functions.write_file import write_file, schema_write_file
from functions.run_python_file import run_python_file, schema_run_python_file

system_prompt = """
You are a helpful AI coding agent.

When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

- List files and directories
- Read file contents
- Execute python files with optional arguments
- Write or overwrite files

All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
"""

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
available_functions = types.Tool(
    function_declarations=[
        schema_get_files_info,
        schema_get_files_content,
        schema_write_file,
        schema_run_python_file
    ]
)

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.0-flash-001', 
    contents=messages, 
    config=types.GenerateContentConfig(
        tools=[available_functions], 
        system_instruction=system_prompt
    )
) 
if num_arguments > 2 and sys.argv[2] == "--verbose":
    print(response.text)
    print(f"User prompt: {user_prompt}")
    print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
else: 
    if response.function_calls:
        print(f"Calling function: {response.function_calls[0].name}({response.function_calls[0].args})") #TODO This will print the wrong info if more than one function is ran 
    else:
        print(response.text)