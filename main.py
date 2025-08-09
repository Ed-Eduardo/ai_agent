import os
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import get_files_info,schema_get_files_info
from functions.get_files_content import get_file_content, schema_get_file_content
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
        schema_get_file_content,
        schema_write_file,
        schema_run_python_file
    ]
)

functions_dict = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file,
}

def call_function(function_call_part: types.FunctionCall, verbose=False) -> types.Content:
    if verbose == True:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    try:
        function_results = functions_dict[function_call_part.name](working_directory="./calculator", **function_call_part.args)
    except KeyError:
        return types.Content(
            role="tool",
            parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"error": f"Unknown function: {function_call_part.name}"},
                )
            ],
        )
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_call_part.name,
                response={"result": function_results},
            )
        ],
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

is_verbose = False
if num_arguments > 2 and sys.argv[2] == "--verbose":
    is_verbose = True

output = []
if response.function_calls:
    for call in response.function_calls:
        function_call_result= call_function(call, verbose=is_verbose)
        if not function_call_result.parts[0].function_response.response:
            raise Exception(f"Fatal error: Something went wrong while running {call.name}")
        else:
            if is_verbose:
                output.append(f"-> {function_call_result.parts[0].function_response.response}")
else:
    if response.text:
        output.append(response.text)

if is_verbose:
    output.extend([
        f"User prompt: {user_prompt}",
        f"Prompt tokens: {response.usage_metadata.prompt_token_count}",
        f"Response tokens: {response.usage_metadata.candidates_token_count}"
    ])
print(f"{'\n'.join(output).replace('\\n', '\n')}")