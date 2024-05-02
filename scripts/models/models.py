import tempfile


def create_temp_model(model_data: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix='.pt', delete=False) as model_file:
        model_file.write(model_data)
        temp_model_path = model_file.name
    return temp_model_path

