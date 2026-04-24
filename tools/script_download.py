import os
import json
from .script_fetch_url import fetch
from .common import error, join_path, format_name, console, config

success_green = config.colours["success_green"]
warning_orange = config.colours["warning_orange"]

def download_script(script_name: str) -> None:
    script_name = format_name(script_name)
    new_script_directory = f"scripts/{script_name}"
    new_script_data = fetch(script_name)["content"]
    console.print(new_script_data)
    if os.path.exists(new_script_directory):
        console.print(f"[{warning_orange}]Script '{new_script_directory}' already exists. Replace?[/{warning_orange}]")
        do_replace_old = input(">> ").lower() in ["y", "yes"]
        if not do_replace_old:
            error(f"Path '{new_script_directory}' already exists")
    else:
        os.mkdir(new_script_directory)
    json.dump(new_script_data, open(join_path(new_script_directory, f"{script_name}.json"), "w"))
    console.print(f"[{success_green}]Script '{script_name}' successfully downloaded[/{success_green}]")

    format(script_name)

