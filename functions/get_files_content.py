import os
from google import genai
from google.genai import types

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(target_file, "r") as f:
            file_content_string = f.read(10000)
            if len(file_content_string) >= 10000:
                file_content_string = file_content_string + f"...File \"{file_path}\" truncated at 10000 characters]"
            return file_content_string
    except Exception as e:
        return f"Error reading file: {e}"
    
schema_get_files_content = types.FunctionDeclaration(
    name="get_files_content",
    description="Read the content of a file constrained to the working directory. The content is truncated at 10000 Characters",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING, 
                description="The filepath to the file that nees to be read, relative to the working directory."
            ),
        },
    ),
)