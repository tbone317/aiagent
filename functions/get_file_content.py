import os
from config import MAX_CHARS
from google.genai import types

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


schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Retrieves the content (at most {MAX_CHARS} characters) of a specified file within the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to read, relative to the working directory",
            ),
        },
        required=["file_path"],
    ),
)
