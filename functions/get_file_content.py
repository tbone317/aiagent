import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        output = ''
        
        abspath = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abspath, file_path))
        valid_target_file = os.path.commonpath([abspath, target_file]) == abspath

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file, 'r') as f:
            output = f.read(MAX_CHARS)
        # After reading the first MAX_CHARS...
            if f.read(1):
                output += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    
        return output
    except Exception as e:
        return f"Error: {str(e)}"