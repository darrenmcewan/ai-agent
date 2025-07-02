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
