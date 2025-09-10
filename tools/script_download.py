import os
import json
from typing import List
from .script_fetch_url import fetch
from .common import error, join_path, format_name

def download(script_name: str) -> None:
    script_name = format_name(script_name)
    new_script_directory = f"scripts/{script_name}"
    if os.path.exists(new_script_directory):
        error(f"Path '{new_script_directory}' already exists")
    os.mkdir(new_script_directory)
    json.dump(fetch(script_name), open(join_path(new_script_directory, f"{script_name}.json"), "w"))
