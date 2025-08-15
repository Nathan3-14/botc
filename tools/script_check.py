import json
from sys import argv
from .common import SCRIPTS_PATH, join_path

def check(script_name: str) -> bool:
    current_script_directory = join_path(SCRIPTS_PATH, script_name)
    current_script_path = join_path(current_script_directory, f"{script_name}.json")
    try:
        script = json.load(open(current_script_path, "r"))
    except FileNotFoundError:
        print(f"File '{current_script_path}' does not exist")
        quit()
    
    character_check_list = json.load(open("tools/data/characters.json", "r"))
    travellers_list = json.load(open("tools/data/travellers.json", "r"))
    fabled_list = json.load(open("tools/data/fabled.json", "r"))
    
    valid = True
    for character in script:
        id = character["id"]
        if id == "_meta":
            continue
        if id not in character_check_list and id not in travellers_list and id not in fabled_list:
            print(f"Script is invalid, character '{id}' cannot be used")
            valid = False
    
    if valid:
        print(f"Script is usable!")
    
    return valid

if __name__ == "__main__":
    args = argv[1:]
    if len(args) != 1:
        print("Invalid args")
        quit()
    
    check(args[0])
