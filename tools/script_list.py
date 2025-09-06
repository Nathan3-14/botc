import json
from typing import Dict, List
from .common import join_path, SCRIPTS_PATH
from rich.console import Console

console = Console()
colours = {
    "townsfolk": "#005fd7",
    "outsider": "#00afaf",
    "minion": "#ff8700",
    "demon": "#cb0e0e",
    "travellers": "#d7afff",
    "fabled": "#ffff5f"
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
    fabled_list = json.load(open("tools/data/fabled.json", "r"))
    travellers_list = json.load(open("tools/data/travellers.json", "r"))
    
    outputs: Dict[str, List[str]] = {
        "townsfolk": [],
        "outsider": [],
        "minion": [],
        "demon": [],
        "fabled": [],
        "travellers": []
    }
    for character in script:
        if type(character) == dict:
            id = character["id"]
            if id == "_meta":
                continue
            if id in travellers_list:
                outputs["travellers"].append(id)
            elif id in fabled_list:
                outputs["fabled"].append(id)
            elif id in character_data.keys():
                outputs[character_data[id]].append(id)
            else:
                print(f"Invalid character '{id}'")
                quit()
    
    for character_type, character_list in outputs.items():
        if len(character_list) == 0:
            continue
        console.print(f"{"-"*20}\n[{colours[character_type]} bold]{character_type.capitalize()}[/{colours[character_type]} bold]")
        for character in character_list:
            console.print(f"[{colours[character_type]}]- {character}[/{colours[character_type]}]")
