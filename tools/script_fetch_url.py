from typing import Dict
import requests
import json
from .common import console

def fetch(search: str) -> Dict:
    console.print(f"https://www.botcscripts.com/api/scripts/?search={search}")
    result = requests.get(f"https://www.botcscripts.com/api/scripts/?search={search}")
    data = json.loads(result.content)
    current_script_data = data["results"][0]
    is_correct = input(f"Did you mean '{current_script_data["name"]} ({current_script_data["version"]})' by '{current_script_data["author"]}'\n>> ").lower() in ["y", "yes", ""]
    if not is_correct:
        console.print("\n" + "\n".join([f"{index}: {item["name"]}" for index, item in enumerate(data["results"][1:])]))
        option = "not a digit"
        while not option.isdigit():
            option = input(f"\nEnter an index of another or 'exit' to exit\n>> ")
            if option.lower() in ["n", "no", "quit", "exit", "q", "e"]:
                quit()
        current_script_data = data["results"][int(option)+1]
    return current_script_data
