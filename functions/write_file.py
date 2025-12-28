import os

def write_file(working_directory, file_path, content):
    try:  
        abspath = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abspath, file_path))
        valid_target_file = os.path.commonpath([abspath, target_file]) == abspath

        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        if not os.path.isdir(os.path.dirname(target_file)):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        
        with open(target_file, 'w') as f:
            f.write(content)
        
        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {str(e)}"