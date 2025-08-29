import json
import os
from pprint import pprint
import requests
from tools import check, format, join_path, search
from tools.common import SCRIPTS_PATH, CURRENT_PATH
from sys import argv

if __name__ == "__main__":
    args = argv[1:]
    if (len(args) != 2) and args[0] != "search":
        print("Invalid args provided")
        quit()
    
    match args[0]:
        case "new" | "download":
            if args[0] == "download":
                result = requests.get(f"https://www.botcscripts.com/api/scripts/?search={args[1]}")
                data = json.loads(result.content)
                current_script_data = data["results"][0]
                is_correct = input(f"Did you mean '{current_script_data["name"]} ({current_script_data["version"]})' by '{current_script_data["author"]}'\n>> ").lower() in ["y", "yes", ""]
                if not is_correct:
                    print("\n" + "\n".join([f"{index}: {item["name"]}" for index, item in enumerate(data["results"][1:])]))
                    option = "not a digit"
                    while not option.isdigit():
                        option = input(f"\nEnter an index of another or 'exit' to exit\n>> ")
                        if option.lower() in ["n", "no", "quit", "exit", "q", "e"]:
                            quit()
                    current_script_data = data["results"][int(option)+1]
                new_file_name = f"{current_script_data["name"].lower().replace(" ", "_")}.json"
                args[1] = new_file_name
                if os.path.exists(new_file_name):
                    do_remove_file = input(f"File '{new_file_name}' already exists, this action will overide it. Continue (y/n) ").lower() in ["yes", "y"]
                    if not do_remove_file:
                        quit()
                json.dump(current_script_data["content"], open(new_file_name, "w"))
            
            if not os.path.exists(args[1]):
                print(f"File '{args[1]}' doesn't exist")
                quit()
            current_script_file = args[1]
            current_script_name = ".".join(current_script_file.split(".")[:-1]).strip("./\\")
            current_script_path = join_path(SCRIPTS_PATH, current_script_name)
            if not os.path.exists(current_script_path):
                os.mkdir(current_script_path)
            new_script_path = join_path(current_script_path, f"{current_script_name}.json")
            if os.path.exists(new_script_path):
                do_remove_file = input(f"A script already exists with the name '{current_script_name}', this action will overide it. Continue (y/n) ").lower() in ["yes", "y"]
                if not do_remove_file:
                    quit()
                os.remove(new_script_path)
            os.rename(join_path(CURRENT_PATH, args[1]), new_script_path)
            if not check(current_script_name):
                quit()
            format(current_script_name)
        case "check":
            check(args[1])
        case "format":
            format(args[1])
        case "search":
            includes = [item for item in args[1:] if not item.startswith("!")]
            excludes = [item[1:] for item in args[1:] if item.startswith("!")]
            print("\n".join(search(includes=includes, excludes=excludes)))
        case _:
            print(f"Invalid option '{args[0]}', expected 'new', 'check' or 'format'")
            quit()
    
    
    
