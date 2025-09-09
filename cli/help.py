import json
from typing import Any, Dict, List
from .common import console, error
import jsonschema
from rich.console import Console
console = Console()

def get_display_args(args: Dict[str, Dict[str, str|bool]], extra_details:bool=True) -> List[str]:
        display_args = []
        for arg_name, arg_details in args.items():
            if arg_details["required"]:
                display_args.append(f"<{arg_name}{f":{arg_details["type"]}" if extra_details else ""}>")
            else:
                display_args.append(f"\\[{arg_name}{f":{arg_details["type"]}" if extra_details else ""}]")
        return display_args
    

class Help:
    def __init__(self, help_dict: Dict[str, Any]) -> None:
        try:
            jsonschema.validate(help_dict, json.load(open("cli/command.schema.json", "r")))
        except jsonschema.ValidationError:
            error(f"Provided dict is not valid")
            ...
        self.help_dict = help_dict | {
            "help": {
                "args": {
                    "command": {
                        "type": "string",
                        "required": False
                    }
                },
                "description_short": "Gets help",
            }
        }
        if "$schema" in self.help_dict.keys():
            self.help_dict.pop("$schema")
        self.commands = [key for key in self.help_dict.keys() if key != "$schema"]
        self.aliases: Dict[str, str] = {}
        self.get_aliases()

    def get_aliases(self) -> None:
        for index in range(len(self.commands)):
            command = self.commands[index]
            if "aliases" in self.help_dict[command]:
                command_aliases = self.help_dict[command]["aliases"]
                if len(command_aliases) > 0:
                    for alias in command_aliases:
                        if alias in self.aliases.keys():
                            error(f"Invalid alias '{alias}', already exists")
                            # print("bad alias")
                            # quit()
                        self.aliases[alias] = command

    def convert_types(self, command_name: str, args: List[Any]) -> List[Any]:
        command_args = self.get_help_details(command_name)["args"]
        new_args = []
        for index, arg in enumerate(args):
            new_type = str
            match command_args[list(command_args.keys())[index]]["type"]:
                case "string": new_type = str
                case "int": new_type = int #type:ignore
                case "bool": new_type = bool #type:ignore
            try:
                new_args.append(new_type(arg))
            except TypeError:
                error(f"Cannot convert '{arg}' to required type '{new_type.__name__}'") #type:ignore
            except IndexError:
                error(f"Too few arguments provided, expected {len(command_args)} but recieved {len(args)}")
        return new_args

    def get_root_command(self, command_name: str) -> str:
        if command_name in self.aliases.keys():
            return self.aliases[command_name]
        if command_name in self.commands:
            return command_name
        error(f"Invalid command '{command_name}'")
        return "" #? Never reached, only used to stop errors

    def get_help_details(self, command_name: str) -> Dict:
        return self.help_dict[self.get_root_command(command_name)]

    def get_help(self, command_name: str="") -> None:
        if command_name == "":
            for command_name, command_details in self.help_dict.items():
                display_args = get_display_args(command_details["args"], extra_details=False)
                console.print(f"[dark_cyan]{command_name} {" ".join(display_args)}{" " if len(display_args) != 0 else ""}[/dark_cyan]- {command_details["description_short"]}", highlight=False)
        else:
            if command_name not in self.help_dict.keys():
                if command_name not in self.aliases.keys():
                    error(f"No command with name '{command_name}', run 'help' for help")
                    # print(f"no command called '{command_name}'")
                    # quit()
                else:
                    command_name = self.aliases[command_name]

            command_details = self.get_help_details(command_name)
            display_args = get_display_args(command_details["args"])
            console.print(command_name)
            console.print(f"Usage: [dark_cyan]{command_name} {" ".join(display_args)}{" " if len(display_args) != 0 else ""}[/dark_cyan]", highlight=False)
            console.print(f"Description: {command_details["description" if "description" in command_details.keys() else "description_short"]}", highlight=False)
            if "aliases" in command_details.keys():
                if len(command_details["aliases"]) > 0:
                    console.print(f"Aliases: {", ".join(command_details["aliases"])}")

if __name__ == "__main__":
    help_dict = json.load(open("test/test_help_dict.json", "r"))
    help_dict.pop("$schema")
    temp_help = Help(help_dict)
    temp_help.get_help()
    print("\n*****\n")
    temp_help.get_help("subtract")
    print("\n*****\n")
    temp_help.get_help("sub")
