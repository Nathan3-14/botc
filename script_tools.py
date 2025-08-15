import os
from tools import check, format, join_path
from tools.common import SCRIPTS_PATH, CURRENT_PATH
from sys import argv

if __name__ == "__main__":
    args = argv[1:]
    if len(args) != 2:
        print("Invalid args provided")
        quit()
    
    match args[0]:
        case "new":
            if not os.path.exists(args[1]):
                print(f"File '{args[1]}' doesn't exist")
                quit()
            current_script_file = args[1]
            current_script_name = ".".join(current_script_file.split(".")[:-1]).strip("./\\")
            print(current_script_name)
            current_script_path = join_path(SCRIPTS_PATH, current_script_name)
            if not os.path.exists(current_script_path):
                os.mkdir(current_script_path)
            os.rename(join_path(CURRENT_PATH, args[1]), join_path(current_script_path, f"{current_script_name}.json"))
            if not check(current_script_name):
                quit()
            format(current_script_name)
        case "check":
            check(args[1])
        case "format":
            format(args[1])
        case _:
            print(f"Invalid option '{args[0]}', expected 'new', 'check' or 'format'")
            quit()
    
    
    
