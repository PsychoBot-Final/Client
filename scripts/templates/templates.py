import os
import shutil
import zipfile
import tempfile
from constants import TEMPLATES_DIR_PATH


def templates_dir_exists(file_name: str) -> bool:
    return os.path.isdir(os.path.join(TEMPLATES_DIR_PATH, file_name))

def unzip_templates(file_name: str, file_data: bytes) -> str:
    file_name = file_name.replace('.zip', '') if file_name.endswith('.zip') else file_name
    fd, tmp_file_path = tempfile.mkstemp()
    os.close(fd)
    dir_path = os.path.join(TEMPLATES_DIR_PATH, file_name)
    try:
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)

        with open(tmp_file_path, 'wb') as tmp_file:
            tmp_file.write(file_data)

        with zipfile.ZipFile(tmp_file_path, 'r') as zip_ref:
            zip_ref.extractall(TEMPLATES_DIR_PATH)
    except zipfile.BadZipFile:
        print("Failed to unzip: Corrupted zip file.")
        return None
    except PermissionError:
        print(f"Permission error: Cannot write to {TEMPLATES_DIR_PATH}.")
        return None
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None
    finally:
        os.unlink(tmp_file_path)
    return dir_path

def remove_templates_dir(dir_name: str) -> None:
    try:
        shutil.rmtree(os.path.join(TEMPLATES_DIR_PATH, dir_name))
    except Exception as e:
        print('Error removing templates directory:', e)