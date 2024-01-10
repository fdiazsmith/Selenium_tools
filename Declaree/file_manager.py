import mimetypes
import os
import sys

class Tempdir:
    def __init__(self, path):
        self.path = path
        self.create_directory()
        self.delete_all_files()

    def create_directory(self):
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    def delete_directory(self):
        if os.path.exists(self.path):
            os.rmdir(self.path)

    def delete_file(self, filename):
        filepath = f'{self.path}/{filename}'
        if os.path.exists(filepath):
            os.remove(filepath)

    def create_file(self, filename):
        filepath = f'{self.path}/{filename}'
        if os.path.exists(filepath):
            print("File already exists")
            return
        with open(filepath, 'w') as f:
            f.write("")
    
    def rename_file(self, filename, new_filename):
        # keep extension
        extension = filename.split('.')[-1]
        new_filepath = f'{self.path}/{new_filename}.{extension}'
        filepath = f'{self.path}/{filename}'
        if os.path.exists(filepath):
            os.rename(filepath, new_filepath)
            
    def delete_all_files(self):
        for filename in os.listdir(self.path):
            filepath = f'{self.path}/{filename}'
            if os.path.exists(filepath):
                os.remove(filepath)
    def get_file_mime_type(self, filename):
        filepath = f'{self.path}/{filename}'
        if os.path.exists(filepath):
            return mimetypes.guess_type(filepath)[0]
        return None
    def get_dir_path(self):
        return self.path   
    def get_full_path(self, filename):
        return f'{self.path}/{filename}'

    def write_to_file(self, filename, data):
        filepath = f'{self.path}/{filename}'
        if not os.path.exists(filepath):
            print("File does not exist")
            return
        with open(filepath, 'w') as f:
            f.write(data)

    def read_file(self, filename):
        filepath = f'{self.path}/{filename}'
        if not os.path.exists(filepath):
            print("File does not exist")
            return
        with open(filepath, 'r') as f:
            return f.read()

    def list_files(self):
        return os.listdir(self.path)

    def list_files_with_extension(self, extension):
        return [filename for filename in os.listdir(self.path) if filename.endswith(extension)]

    def list_files_with_prefix(self, prefix):
        return [filename for filename in os.listdir(self.path) if filename.startswith(prefix)]

    def list_files_with_prefix_and_extension(self, prefix, extension):
        return [filename for filename in os.listdir(self.path) if filename.startswith(prefix) and filename.endswith(extension)]

    def list_files_with_extension_and_prefix(self, extension, prefix):
        return [filename for filename in os.listdir(self.path) if filename.startswith(prefix) and filename.endswith(extension)]

    def list_files_with_extension_and_prefix(self, extension, prefix):
        return [filename for filename in os.listdir(self.path) if filename.startswith(prefix) and filename.endswith(extension)]

    def list_files_with_extension_and_prefix(self, extension, prefix):
        return [filename for filename in os.listdir(self.path) if filename.startswith(prefix) and filename.endswith(extension)]

    def list_files_with_extension_and_prefix(self, extension, prefix):
        return [filename for filename in os.listdir(self.path) if filename.startswith(prefix) and filename.endswith(extension)]