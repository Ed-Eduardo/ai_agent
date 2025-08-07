import os
import subprocess
from google import genai
from google.genai import types

def run_python_file(working_directory, file_path, args=[]):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.exists(target_file):
        return f'Error: File "{file_path}" not found.'
    if not target_file.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    target_file_dir = "/".join(target_file.split("/")[:-1])
    commands = ['python', file_path] + args
    try: 
        test = subprocess.run(commands, cwd=working_directory,  timeout=30, capture_output=True, )
        stdout = test.stdout.decode('utf-8')
        stderr = test.stderr.decode('utf-8')

        output = [f"STDOUT:\n{stdout}", f"STDERR:\n{stderr}"]

        error_code = test.returncode
        if error_code != 0:
            error_code = f"Process exited with code {error_code}"
            output.append(error_code)
        
        return "\n".join(output)
    except Exception as e:
        return f"Error: executing python file: {e}"

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs an existing file with optinal args, provided it has a .py extension and resides in the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING, 
                description="The file path to the python file that needs to be ran"
            ),
            "args": types.Schema(
                type=types.Type.STRING, 
                description="The args to pass to the executing python file"
            ),
        },
    ),
)