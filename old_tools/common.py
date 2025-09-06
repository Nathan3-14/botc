import os
from rich.console import Console
from .colours import error_red

def join_path(path: str, *paths: str):
    return os.path.normpath(os.path.join(path, *paths))

def error(message: str, _quit: bool=True):
    console.print(f"[{error_red} bold]{message}[/{error_red} bold]")
    if _quit:
        quit()

CURRENT_PATH = os.getcwd()
SCRIPTS_PATH = join_path(CURRENT_PATH, "scripts")
console = Console()

