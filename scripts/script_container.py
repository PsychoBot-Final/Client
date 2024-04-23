class ScriptContainer:
    def __init__(self, version: float, file_name: str, class_: str, source: str, model: bytes, templates: bytes) -> None:
        self.version = version
        self.file_name = file_name
        self.class_ = class_
        self.source = source
        self.model = model
        self.templates = templates