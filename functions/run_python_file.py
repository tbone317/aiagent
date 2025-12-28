import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:

        abspath = os.path.abspath(working_directory)
        target_file = os.path.normpath(os.path.join(abspath, file_path))
        valid_target_file = os.path.commonpath([abspath, target_file]) == abspath

        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        if not os.path.isfile(target_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith('.py'):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python3", target_file]
        if args:
            command.extend(args)
        
        result = subprocess.run(command, capture_output=True, text=True, cwd=abspath, timeout=30)
        if result.returncode != 0:
            return f"Process exited with code {result.returncode}"
        if result.stdout is None or result.stdout.strip() == "" or result.stderr.strip() != "":
            return "No output produced"
        
        output = f"STDOUT: {result.stdout.strip()}\nSTDERR: {result.stderr.strip()}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"