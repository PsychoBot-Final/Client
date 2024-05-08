import os
import cv2 as cv
from constants import TEMPLATES_DIR_PATH, VALID_TEMPLATE_EXTENSIONS


def load_templates(dir_name: str) -> dict:
    templates = {}
    templates_dir = os.path.join(TEMPLATES_DIR_PATH, dir_name)
    for template in os.listdir(templates_dir):
        name, ext = os.path.splitext(template)
        if ext.lower() in VALID_TEMPLATE_EXTENSIONS:
            template_path = os.path.join(templates_dir, template)
            if not name in templates:
                templates[name] = cv.imread(template_path, cv.IMREAD_UNCHANGED)