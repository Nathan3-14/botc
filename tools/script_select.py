import os
from typing import Any, List

from matplotlib.layout_engine import ConstrainedLayoutEngine
from .common import SCRIPTS_PATH, get_character_list, load_script

def compare(list_1: List[Any], list_2: List[Any]) -> bool:
    for val in list_1:
        if val in list_2:
            return True
    return False



def select_scripts(initial_script_path: str, count: int=3) -> List[str]:
    #TODO make recursive for all given paths and return all sets
    scripts = [initial_script_path]
    current_characters = [get_character_list(load_script(initial_script_path))]
    index = 0
    scripts = os.listdir(SCRIPTS_PATH)
    while len(scripts) < count:
        current_script = get_character_list(load_script(scripts[index]))
        if compare(current_script, current_characters):
            continue
        current_characters += current_script
    
    return scripts