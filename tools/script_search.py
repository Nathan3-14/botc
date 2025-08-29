import json
import os
import pprint
from typing import Dict, List
from .common import SCRIPTS_PATH, join_path

def search(includes: List[str]=[], excludes: List[str]=[]) -> List[str]:
    valid_scripts = []
    for script_folder in os.listdir(SCRIPTS_PATH):
        is_invalid = False
        raw_data: List[Dict[str, str]] = json.load(open(join_path(SCRIPTS_PATH, script_folder, f"{script_folder}.json"), "r"))
        for item in raw_data:
            if type(item) == str:
                character_ids = [item for item in raw_data if type(item) != dict]
                break
        else:
            character_ids = [item["id"] for item in raw_data if item["id"] != "_meta"] #type:ignore
            
        for include_id in includes:
            is_invalid = (include_id not in character_ids) or is_invalid
        for exclude_id in excludes:
            is_invalid = (exclude_id in character_ids) or is_invalid
        if is_invalid:
            continue
        valid_scripts.append(script_folder)
    return valid_scripts