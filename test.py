import hashlib
import os
from util import get_resource_path


def hash_all_files(directory, hash_type='sha256'):
    all_hashes = []
    skip_dirs = {'__pycache__', 'venv', '.git'}  # Directories to skip
    skip_extensions = {'.pyc'}  # File extensions to skip
    skip_files = {'.env', '.gitignore'}

    for root, dirs, files in os.walk(directory, topdown=True):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        for filename in files:
            if filename in skip_files:
                continue
            extension = os.path.splitext(filename)[1].lower()
            if extension in skip_extensions:
                continue
            filepath = os.path.join(root, filename)
            hash_obj = hashlib.new(hash_type)
            try:
                with open(filepath, 'rb') as file:
                    for chunk in iter(lambda: file.read(4096), b""):
                        hash_obj.update(chunk)
                    all_hashes.append(hash_obj.hexdigest())
            except Exception as e:
                print(f"Error processing file {filepath}: {e}")

    combined_hash_obj = hashlib.new(hash_type)
    for file_hash in all_hashes:
        combined_hash_obj.update(file_hash.encode('utf-8'))
    final_hash = combined_hash_obj.hexdigest()
    print('Final Hash:', final_hash)
    return final_hash