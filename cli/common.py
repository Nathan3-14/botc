import os
from rich.console import Console
from .colours import error_red

def error(message: str, _quit: bool=True):
    console.print(f"[{error_red} bold]{message}[/{error_red} bold]")
    if _quit:
        quit()

console = Console()

