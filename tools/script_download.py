import os
import json
from .script_fetch_url import fetch
from .common import error, join_path, format_name, console, config
from .script_check import check_file
from .script_format import format

success_green = config.colours["success_green"]

def download(script_name: str, ignore_check: bool=False) -> None:
    script_name = format_name(script_name)
    new_script_directory = f"scripts/{script_name}"
    new_script_data = fetch(script_name)["content"]
    console.print(new_script_data)
    if not ignore_check:
        if not check_file(new_script_data):
            error("New script is invalid")
    if os.path.exists(new_script_directory):
        error(f"Path '{new_script_directory}' already exists")
    os.mkdir(new_script_directory)
    json.dump(new_script_data, open(join_path(new_script_directory, f"{script_name}.json"), "w"))
    console.print(f"[{success_green}]Script '{script_name}' successfully downloaded[/{success_green}]")

    format(script_name)

