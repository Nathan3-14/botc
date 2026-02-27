import os
from typing import Any, List, Tuple
from .common import SCRIPTS_PATH, get_character_list, load_script, console, warning_orange

def has_overlaps(list_1: List[Any], list_2: List[Any], overlap_max: int=0, starting_overlaps: int=0) -> Tuple[bool, int]:
    overlaps = starting_overlaps
    for val in list_1:
        if val in list_2:
            overlaps += 1
    if overlaps > overlap_max:
        return True, overlaps
    return False, overlaps

# def select_script_route(current_script_sets: List[List[str]], current_characters: List[str], count: int) -> List[str]:
#     return ["!!TESTING!!"]

def find_scripts(current_scripts: List[str], current_characters: List[str], count: int, overlap_max: int, current_overlaps: int) -> List[List[str]]:
    if len(current_scripts) >= count:
        return [current_scripts]
    to_return = []
    for script in os.listdir(SCRIPTS_PATH):
        script_character_list = get_character_list(load_script(script))
        
        has_too_many_overlaps, overlap_count = has_overlaps(script_character_list, current_characters, overlap_max)
        if has_too_many_overlaps:
            continue
        current_overlaps += overlap_count
            

        to_return += find_scripts(
            current_scripts + [script],
            current_characters + script_character_list,
            count,
            overlap_max,
            current_overlaps
        )
    
    return to_return

colours = [
    "#e57373",
    "#f06292",
    "#9575cd",
    "#7986cb",
    "#64b5f6",
    "#dce775",
    "#aed581",
    "#81c784",
    "#4db6ac",
    "#4dd0e1",
    "#4fc3f7"
]

def select_scripts(initial_script_path: str, count: int=3, overlap_maximum: int=0) -> None:
    if initial_script_path == ".":
        script_sets = find_scripts([], [], count, overlap_maximum, 0)
    else:
        current_characters = get_character_list(load_script(initial_script_path))
        script_sets = find_scripts([initial_script_path], current_characters, count, overlap_maximum, 0)
    if len(script_sets) == 0:
        console.print(f"[{warning_orange}]No Script Sets of {count} found containing {initial_script_path}[/{warning_orange}]")
        return
    print(f"Script Sets of {count} that contain {initial_script_path if initial_script_path != "." else "any scripts"} with a maximum number of {overlap_maximum} overlaping characters are:")
    selected_colours = {}
    for script_set in script_sets:
        line = "    "
        for script_name in script_set:
            if script_name not in selected_colours.keys():
                selected_colours[script_name] = colours[len(selected_colours.keys())%len(colours)]
            line += f"[{selected_colours[script_name]}]{script_name}[/{selected_colours[script_name]}] "
        console.print(line)