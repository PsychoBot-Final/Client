class ScriptContainer:
    def __init__(self, version: float, file_name: str, module_class: str, source: str, model_path: str, templates_path: str) -> None:
        self.version = version
        self.file_name = file_name
        self.module_class = module_class
        self.source = source
        self.model_path = model_path
        self.templates_path = templates_path