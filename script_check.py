import json
from sys import argv

if __name__ == "__main__":
    args = argv[1:]
    if len(args) != 1:
        print("Invalid args")
        quit()
    
    if ".json" in args[0]:
        path = args[0]
    else:
        path = f"scripts/{args[0]}/{args[0]}.json"
    try:
        script = json.load(open(path, "r"))
    except FileNotFoundError:
        print(f"File './{path}' does not exist")
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
