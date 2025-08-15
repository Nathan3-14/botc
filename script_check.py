import json
from sys import argv
import os

if __name__ == "__main__":
    current_path = os.getcwd()
    scripts_path = os.path.join(current_path, "scripts")

    args = argv[1:]
    if len(args) != 1:
        print("Invalid args")
        quit()
    
    current_script_directory = os.path.join(scripts_path, args[0])
    current_script_path = os.path.join(current_script_directory, args[0] + "" if args[0].endswith(".json") else ".json")
    try:
        script = json.load(open(current_script_path, "r"))
    except FileNotFoundError:
        print(f"File '{current_script_path}' does not exist")
        quit()
    
    character_check_list = json.load(open("characters.json", "r"))
    travellers_list = json.load(open("travellers.json", "r"))
    
    valid = True
    for character in script:
        id = character["id"]
        if id == "_meta":
            continue
        if id not in character_check_list and id not in travellers_list:
            print(f"Script is invalid, character '{id}' cannot be used")
            valid = False
    
    if valid:
        print(f"Script is usable!")
