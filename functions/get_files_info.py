import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        output = ''
        files_info = []
        
        abspath = os.path.abspath(working_directory)
        target_dir = os.path.normpath(os.path.join(abspath, directory))
        valid_target_dir = os.path.commonpath([abspath, target_dir]) == abspath
        
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            if os.path.isfile(item_path):
                size = os.path.getsize(item_path)
                files_info.append({
                    'name': item,
                    'size': size,
                    'is_dir': False
                })
            elif os.path.isdir(item_path):
                size = os.path.getsize(item_path)
                files_info.append({
                    'name': item,
                    'size': size,
                    'is_dir': True
                })
        
        for file_info in files_info:
            output += f"- {file_info['name']}: file_size={file_info['size']} bytes, is_dir={file_info['is_dir']}\n"

        return output
    except Exception as e:
        return f"Error: {str(e)}"

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)