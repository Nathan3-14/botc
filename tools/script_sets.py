import os
from typing import Any, List, Set, Tuple, FrozenSet
from .common import SCRIPTS_PATH, get_character_list, load_script, console, warning_orange

def has_overlaps(list_1: List[Any], list_2: List[Any], overlap_max: int=0, starting_overlaps: int=0) -> Tuple[bool, int]:
    overlaps = starting_overlaps
    for val in list_1:
        if val in list_2:
            overlaps += 1
    if overlaps > overlap_max:
        return True, overlaps
    return False, overlaps

def find_script_sets(current_scripts: List[str], current_characters: List[str], count: int, overlap_max: int, current_overlaps: int) -> Set[FrozenSet[str]]:
    if len(current_scripts) >= count:
        return {frozenset(current_scripts)}
    to_return = set()
    for script in os.listdir(SCRIPTS_PATH):
        script_character_list = get_character_list(load_script(script))
        
        has_too_many_overlaps, overlap_count = has_overlaps(script_character_list, current_characters, overlap_max)
        if has_too_many_overlaps:
            continue
        current_overlaps += overlap_count
        

        to_return.update(find_script_sets(
            current_scripts + [script],
            current_characters + script_character_list,
            count,
            overlap_max,
            current_overlaps
        ))
    
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

def get_script_sets(count: int=3, overlap_maximum: int=0, export: bool=False) -> None:
    script_sets = find_script_sets([], [], count, overlap_maximum, 0)

    if len(script_sets) == 0:
        console.print(f"[{warning_orange}]No Script Sets of {count} with a maximum number of {overlap_maximum} overlaping characters[/{warning_orange}]")
        return

    #* Display Scripts in a Cool Manner *#
    print(f"Script Sets of {count} with a maximum number of {overlap_maximum} overlaping characters are:")
    selected_colours = {}
    for script_set in script_sets:
        line = "    "
        for script_name in script_set:
            if script_name not in selected_colours.keys():
                selected_colours[script_name] = colours[len(selected_colours.keys())%len(colours)]
            line += f"[{selected_colours[script_name]}]{script_name}[/{selected_colours[script_name]}] "
        console.print(line)
    
    if export:
        with open(f"script_sets.txt", "w") as f:
            for script_set in script_sets:
                f.write(", ".join(script_set) + "\n")