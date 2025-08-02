import os 

def get_dir_contents(directory): 
    pass

def get_files_info(working_directory, directory="."):
    current_dir = os.path.join(working_directory, directory)

    match current_dir:
        case dir if dir not in working_directory:
            f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        case dir if os.path.isdir(dir) != True:
            f'Error: "{directory}" is not a directory'
        case _: 
            pass