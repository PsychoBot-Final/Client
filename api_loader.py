import sys
import importlib.util
from base64 import b64decode
from types import ModuleType
from constants import API_PACKAGE_NAME


if API_PACKAGE_NAME not in sys.modules:
    package = ModuleType(API_PACKAGE_NAME)
    sys.modules[API_PACKAGE_NAME] = package
else:
    package = sys.modules[API_PACKAGE_NAME]

if not hasattr(package, 'modules'):
    package.modules = {}

def receive_api(data: any) -> None:
    files = data['files']
    for file in files:
        code = b64decode(file['content']).decode('utf-8')
        module_name = str(file['filename']).replace('.py', '')
        full_module_name = f"{API_PACKAGE_NAME}.{module_name}"
        print(full_module_name)
        spec = importlib.util.spec_from_loader(full_module_name, loader=None)
        module = importlib.util.module_from_spec(spec)
        exec(code, module.__dict__)
        package.modules[module_name] = module
        sys.modules[full_module_name] = module

# def receive_api(data) -> None:
#     files = data['files']
#     print('Total Files:', len(files))
#     for file in files:
#         code = b64decode(file['content']).decode('utf-8')
#         module_name = str(file['filename']).replace('.py', '')
#         print('API Module:', module_name)
#         spec = importlib.util.spec_from_loader(module_name, loader=None)
#         module = importlib.util.module_from_spec(spec)
#         exec(code, module.__dict__)
#         modules[module_name] = module
#         sys.modules[module_name] = module
        