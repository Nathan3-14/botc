import os
from re import S
from typing import Any, Dict
from rich.console import Console
import tomllib

class Config:
    def __init__(self, config_dict: Dict[str, Dict[str, str]]) -> None:
        self.character_colours = config_dict["character_colours"]
        self.colours = config_dict["colours"]

config = Config(tomllib.load(open("tools/config.toml", "rb")))
error_red = config.colours["error_red"]

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

CURRENT_PATH = os.getcwd()
SCRIPTS_PATH = join_path(CURRENT_PATH, "scripts")
console = Console()

