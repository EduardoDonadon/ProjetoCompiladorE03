import os
from contextlib import contextmanager


class FileManagement:
    def check_file_exists(self, path):
        if os.path.isabs(path):
            full_path = path
        else:
            current_directory = os.getcwd()
            full_path = os.path.join(current_directory, path)

        if os.path.exists(full_path):
            if os.path.isfile(full_path):
                _, file_extension = os.path.splitext(full_path)
                if file_extension == ".232":
                    return True
                else:
                    print(
                        f"The file extension '{file_extension}' does not "
                        "match with .232"
                    )
            else:
                print(f"The path '{full_path}' exists, but it is not a file.")
        else:
            print(f"The path '{full_path}' does not exist.")

        return False

    @contextmanager
    def open_file(self, file_path, mode="r"):
        file = None
        try:
            file = open(file_path, mode)
            yield file
        except Exception as error:
            print(f"An error occurred while opening the file: {error}")
            raise
        finally:
            if file:
                file.close()
