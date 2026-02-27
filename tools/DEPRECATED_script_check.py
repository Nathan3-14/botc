import json
from typing import Dict, List
from warnings import deprecated
from .common import SCRIPTS_PATH, get_character_list, join_path, console, error, config

success_green = config.colours["success_green"]

def check_script(script_json: List[str|Dict[str,str]]) -> bool:
    character_check_list = list(json.load(open("tools/data/characters.json", "r")).keys())
    travellers_list = json.load(open("tools/data/travellers.json", "r"))
    fabled_list = json.load(open("tools/data/fabled.json", "r"))
    
    valid = True
    for character in get_character_list(script_json, True, True):
        if character not in character_check_list and character not in travellers_list and character not in fabled_list:
            error(f"Script is invalid, character '{character}' cannot be used", _quit=False)
            valid = False
    
    if valid:
        console.print(f"[{success_green}]Script is usable![/{success_green}]")
    
    return valid

def check(script_name: str) -> bool:
    current_script_directory = join_path(SCRIPTS_PATH, script_name)
    current_script_path = join_path(current_script_directory, f"{script_name}.json")
    try:
        script = json.load(open(current_script_path, "r"))
    except FileNotFoundError:
        error(f"File '{current_script_path}' does not exist")
        quit()
    
    return check_script(script)

