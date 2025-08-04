import os 

def write_file(working_directory, file_path, content):
    abs_working_dir = os.path.abspath(working_directory)
    target_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    if not target_file_path.startswith(abs_working_dir):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    print(f"target_file_path = {target_file_path}")
    target_file_dir = "/".join(target_file_path.split("/")[:-1])
    print(f"target_file_dir = {target_file_dir}")
    print(f"target_file_dir exists = {os.path.exists(target_file_dir)}")
    if not os.path.exists(target_file_dir):
        try:
            os.makedirs(target_file_dir)
        except Exception as e:
            return f"Error creating file path: {e}"
    try:
        with open(target_file_path, "w") as f:
            f.write(content)
            return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error writing file: {e}"

    