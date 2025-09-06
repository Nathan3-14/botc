import json
from sys import argv
from .common import SCRIPTS_PATH, join_path, console, error
from .colours import success_green

def check(script_name: str) -> bool:
    current_script_directory = join_path(SCRIPTS_PATH, script_name)
    current_script_path = join_path(current_script_directory, f"{script_name}.json")
    try:
        script = json.load(open(current_script_path, "r"))
    except FileNotFoundError:
        error(f"File '{current_script_path}' does not exist")
        quit()
    
    character_check_list = list(json.load(open("old_tools/data/characters.json", "r")).keys())
    travellers_list = json.load(open("old_tools/data/travellers.json", "r"))
    fabled_list = json.load(open("old_tools/data/fabled.json", "r"))
    
    valid = True
    for character in script:
        id = character if type(character) == str else character["id"]
        if id == "_meta":
            continue
        if id not in character_check_list and id not in travellers_list and id not in fabled_list:
            error(f"Script is invalid, character '{id}' cannot be used")
            valid = False
    
    if valid:
        console.print(f"[{success_green}]Script is usable![/{success_green}]")
    
    return valid

