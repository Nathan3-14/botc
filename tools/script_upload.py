import json
import os
from .common import error, format_name, console, config, join_path
from .script_check import check_file
from .script_format import format

option_yellow = config.colours["option_yellow"]
success_green = config.colours["success_green"]

def upload(script_file: str) -> None:
    if not os.path.exists(script_file):
        error(f"File '{script_file}' does not exist")

    script_file_formatted = format_name(script_file)
    new_script_name = script_file_formatted[:-5]
    new_script_directory = join_path("scripts", new_script_name)
    new_script_path = join_path(new_script_directory, script_file_formatted)
    if os.path.exists(new_script_directory):
        console.print(f"[{option_yellow}]A script with the name '{new_script_name}' already exists.[/{option_yellow}]")
        console.print(f"[{option_yellow}]This action will override it, continue (y/n)? [/{option_yellow}]", end="")
        do_override = input().lower() in ["y", "yes"]
        if not do_override:
            quit()
    else:
        os.mkdir(new_script_directory)
    os.rename(script_file, new_script_path)
    
    format(new_script_name)
    
