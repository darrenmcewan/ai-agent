import os
def get_files_info(working_directory, directory=None):
    try:
        if directory is None or directory == ".":
            target_directory = working_directory
        else: 
            target_directory = os.path.join(working_directory, directory)

        abs_working_directory = os.path.abspath(working_directory)
        abs_target_directory = os.path.abspath(target_directory)

        if not abs_target_directory.startswith(abs_working_directory):
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_target_directory):
            return f'Error: "{directory}" is not a directory'
 
        file_info_list = []
        for item_name in os.listdir(abs_target_directory):
            item_path = os.path.join(abs_target_directory, item_name)
            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path) if os.path.isfile(item_path) else (0 if not is_dir else 0) # Directories can have size 0, files have actual size
            file_info_list.append(f"- {item_name}: file_size={file_size} bytes, is_dir={is_dir}")

        return "\n".join(file_info_list)

    except FileNotFoundError:
        return f'Error: Directory "{directory}" not found'
    except PermissionError:
        return f'Error: Permission denied to access "{directory}"'
    except Exception as e:
        return f'Error: An unexpected error occurred: {e}'


def get_file_content(working_directory, file_path):
    MAX_CHARS = 10000

    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_directory = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        # Check if the path is a file
        if not os.path.isfile(abs_full_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(abs_full_path, "r") as f:
            content = f.read(MAX_CHARS + 1)  # Read one more character to check for truncation

        if len(content) > MAX_CHARS:
            content = content[:MAX_CHARS] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return content

    except FileNotFoundError:
        return f'Error: File not found: "{file_path}"'
    except PermissionError:
        return f'Error: Permission denied to read "{file_path}"'
    except Exception as e:
        return f'Error: An unexpected error occurred: {e}'



def write_file(working_directory, file_path, content):
    """
    Writes content to a file within a specified working directory.
    Creates the file and its parent directories if they don't exist.
    Overwrites existing content.

    Args:
        working_directory (str): The base directory for file operations.
        file_path (str): The relative path to the file within the working_directory.
        content (str): The content to write to the file.

    Returns:
        str: A success message or an error message.
    """
    try:
        full_path = os.path.join(working_directory, file_path)
        abs_working_directory = os.path.abspath(working_directory)
        abs_full_path = os.path.abspath(full_path)

        # Validate that the file_path is within working_directory boundaries
        if not abs_full_path.startswith(abs_working_directory):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        # Ensure the directory exists
        parent_dir = os.path.dirname(abs_full_path)
        os.makedirs(parent_dir, exist_ok=True)

        with open(abs_full_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except PermissionError:
        return f'Error: Permission denied to write to "{file_path}"'
    except Exception as e:
        return f'Error: An unexpected error occurred: {e}'
