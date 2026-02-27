import json
import os
from typing import Any, Dict, List, List
from rich.console import Console
import tomllib

class Config:
    def __init__(self, config_dict: Dict[str, Dict[str, str]]) -> None:
        self.character_colours = config_dict["character_colours"]
        self.colours = config_dict["colours"]

config = Config(tomllib.load(open("tools/config.toml", "rb")))
error_red = config.colours["error_red"]
warning_orange = config.colours["warning_orange"]

def format_name(script_name: str, to_underscore: bool=True) -> str:
    if to_underscore:
        return script_name.lower().replace(" ", "_")
    else:
        return script_name.lower().replace("_", " ")

def join_path(path: str, *paths: str):
    return os.path.normpath(os.path.join(path, *paths))

def error(message: str, _quit: bool=True):
    console.print(f"[{error_red} bold]{message}[/{error_red} bold]")
    if _quit:
        quit()

def get_character_list(raw_data: List[str|Dict[str, str]], include_travellers: bool=False, include_fabeld=False) -> List[str]:
    character_ids: List[str] = []
    for item in raw_data:
        if type(item) == str:
            character_ids = [item for item in raw_data if type(item) != dict] #type:ignore
            break
    else:
        character_ids = [item["id"] for item in raw_data if item["id"] != "_meta"] #type:ignore
    return character_ids

def load_script(script_name: str) -> List[str|Dict[str, str]]:
    current_script_directory = join_path(SCRIPTS_PATH, script_name)
    current_script_path = join_path(current_script_directory, f"{script_name}.json")
    try:
        script = json.load(open(current_script_path, "r"))
    except FileNotFoundError:
        console.print(f"File '{current_script_path}' does not exist")
        quit()
    return script

CURRENT_PATH = os.getcwd()
SCRIPTS_PATH = join_path(CURRENT_PATH, "scripts")
console = Console()

if __name__ == "__main__":
    print(get_character_list(json.load(open("scripts/who_am_i_/who_am_i_.json", "r"))))
