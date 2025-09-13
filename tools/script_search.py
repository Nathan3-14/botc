import json
import os
from typing import Dict, List
from .common import SCRIPTS_PATH, join_path, console

def display_search(criteria: List[str]) -> None:
    includes = [item for item in criteria if not item.startswith("!")]
    excludes = [item[1:] for item in criteria if item.startswith("!")]
    console.print("\n".join(search(includes, excludes)))

def search(includes: List[str]=[], excludes: List[str]=[]) -> List[str]:
    valid_script_folders = []
    for script_folder in os.listdir(SCRIPTS_PATH):
        raw_data: List[Dict[str, str]] = json.load(open(join_path(SCRIPTS_PATH, script_folder, f"{script_folder}.json"), "r"))
        for item in raw_data:
            if type(item) == str:
                character_ids = [item for item in raw_data if type(item) != dict]
                break
        else:
            character_ids = [item["id"] for item in raw_data if item["id"] != "_meta"] #type:ignore
            
        is_invalid = False
        
        for include in includes:
            at_least_one_is_in = False
            for include_id in include.split("/"):
                at_least_one_is_in = (include_id in character_ids) or at_least_one_is_in
            is_invalid = (not at_least_one_is_in) or is_invalid
        for exclude in excludes:
            for exclude_id in exclude.split("/"):
                is_invalid = (exclude_id in character_ids) or is_invalid
            
        if is_invalid:
            continue
        valid_script_folders.append(script_folder)
    return valid_script_folders