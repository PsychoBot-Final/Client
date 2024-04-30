import os
import sys
import shutil
import zipfile
import tempfile
from constants import TEMPLATES_DIR_PATH


def remove_templates_dir(dir_name: str) -> None:
    try:
        shutil.rmtree(os.path.join(TEMPLATES_DIR_PATH, dir_name))
    except Exception as e:
        print('Error removing templates directory:', e)

def unzip_templates(file_data) -> None:
    fd, tmp_file_path = tempfile.mkstemp()
    print('Temporary file created at:', tmp_file_path)  # Log temp file path
    os.close(fd)
    try:
        with open(tmp_file_path, 'wb') as tmp_file:
            tmp_file.write(file_data)
            print('Data written to temporary file.')

        with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
            print(f'Extracting ZIP to {TEMPLATES_DIR_PATH}')
            zip_ref.extractall(TEMPLATES_DIR_PATH)
            print('Extraction complete.')
    except Exception as e:
        print('Error unzipping:', e)
    finally:
        os.remove(tmp_file_path)
        print('Temporary file removed.')

def get_resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)