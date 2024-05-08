import sys
import importlib.util
from base64 import b64decode

modules = {}

def receive_api(data) -> None:
    files = data['files']
    print('Total Files:', len(files))
    for file in files:
        code = b64decode(file['content']).decode('utf-8')
        module_name = str(file['filename']).replace('.py', '')
        print('API Module:', module_name)
        spec = importlib.util.spec_from_loader(module_name, loader=None)
        module = importlib.util.module_from_spec(spec)
        exec(code, module.__dict__)
        modules[module_name] = module
        sys.modules[module_name] = module
        