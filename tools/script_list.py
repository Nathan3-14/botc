import json
from typing import Dict, List
from .common import join_path, SCRIPTS_PATH
from rich.console import Console

console = Console()
colours = {
    "townsfolk": "#005fd7",
    "outsider": "#00afaf",
    "minion": "#ff8700",
    "demon": "#cb0e0e"
}

def list_script(script_name: str):
    # console.print("a")
    current_script_directory = join_path(SCRIPTS_PATH, script_name)
    current_script_path = join_path(current_script_directory, f"{script_name}.json")
    try:
        script = json.load(open(current_script_path, "r"))
    except FileNotFoundError:
        print(f"File '{current_script_path}' does not exist")
        quit()
    character_data = json.load(open("tools/data/characters.json", "r"))
    
    outputs: Dict[str, List[str]] = {
        "townsfolk": [],
        "outsider": [],
        "minion": [],
        "demon": []
    }
    for character in script:
        if type(character) == dict:
            id = character["id"]
            if id == "_meta":
                continue  
            outputs[character_data[id]].append(id)
    # console.print(outputs)
    for character_type, character_list in outputs.items():
        console.print(f"\n{"-"*20}\n[{colours[character_type]} bold]{character_type.capitalize()}[/{colours[character_type]} bold]")
        for character in character_list:
            console.print(f"[{colours[character_type]}]- {character}[/{colours[character_type]}]")
