from datetime import datetime
import os


def generate_filename_timestamp(file):
    original_name = file.name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    name, ext = os.path.splitext(original_name)
    new_name = f"{name}_{timestamp}{ext}"
    file.name = new_name
    return file
