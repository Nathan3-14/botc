import json
from typing import Dict, List, Literal
from .common import join_path, SCRIPTS_PATH, console, error, config, get_character_list, load_script

colours = config.character_colours

def display_script(script_name: str, character_types: List[Literal["townsfolk", "outsider", "minion", "demon", "travellers", "fabled"]]=["townsfolk", "outsider", "minion", "demon", "travellers", "fabled"]) -> None:
    # current_script_directory = join_path(SCRIPTS_PATH, script_name)
    # current_script_path = join_path(current_script_directory, f"{script_name}.json")
    # try:
    #     script = json.load(open(current_script_path, "r"))
    # except FileNotFoundError:
    #     console.print(f"File '{current_script_path}' does not exist")
    #     quit()
    script = load_script(script_name)
    character_data = json.load(open("tools/data/characters.json", "r")) | json.load(open("tools/data/new_characters.json"))
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
    for character_id in get_character_list(script, True, True):
        # if type(character) == dict:
        #     id = character["id"]
        #     if id == "_meta":
        #         continue
        # elif type(character) == str:
        #     id = character
        # else:
        #     error(f"Invalid type for character: {type(character)}")
        #     quit() #? not actually used, but stops type check complaints
        if character_id in travellers_list:
            outputs["travellers"].append(character_id)
        elif character_id in fabled_list:
            outputs["fabled"].append(character_id)
        elif character_id in character_data.keys():
            outputs[character_data[character_id]].append(character_id)
        else:
            console.print(f"Invalid character: '{character_id}'")
            quit()
    
    for character_type, character_list in outputs.items():
        if character_type not in character_types:
            continue
        console.print(f"{"-"*20}\n[{colours[character_type]} bold]{character_type.capitalize()}[/{colours[character_type]} bold]")
        if len(character_list) == 0:
            console.print(f"[{colours[character_type]}]None[/{colours[character_type]}]")
        for character in character_list:
            console.print(f"[{colours[character_type]}]- {character}[/{colours[character_type]}]")
