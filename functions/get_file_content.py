import os

def get_file_content(working_directory, file_path):
    abs_working_dir = os.path.abspath(working_directory)
    target_file = os.path.abspath(os.path.join(working_directory, file_path))
    print(f"abs_working_dir: {abs_working_dir}")
    print(f"target_file: {target_file}")
    if not target_file.startswith(abs_working_dir):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    if not os.path.isdir(target_file):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    try:
        with open(file_path, "r") as f:
            file_content_string = f.read(10000)
            if len(file_content_string >= 10000):
                file_content_string = file_content_string + f"...File \"{file_path}\" truncated at 10000 characters]"
            return file_content_string
    except Exception as e:
        return f"Error reading file: {e}"
    
