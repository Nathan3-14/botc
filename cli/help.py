import json
from typing import Any, Dict, List
from .common import console, error
from .colours import log_grey
import jsonschema
from rich.console import Console
console = Console()

    

class Help:
    def __init__(self, help_dict: Dict[str, Any]) -> None:
        try:
            jsonschema.validate(help_dict, json.load(open("cli/command.schema.json", "r")))
        except jsonschema.ValidationError:
            error(f"Provided dict is not valid")
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
                        self.aliases[alias] = command

    def get_type(self, type_string: str) -> type:
        match type_string:
            case "string": return str
            case "int": return int
            case "bool": return bool
            case "flag": return int #? not actually converted
            case _: error(f"Invalid type provided '{type_string}'")
        return str #? never actually reached

    def convert_types(self, command_name: str, args: List[Any]) -> List[Any]:
        command_args = self.get_help_details(command_name)["args"]
        new_args: List[Any] = []
        for index, arg in enumerate(args):
            try:
                type_string = command_args[list(command_args.keys())[index]]["type"]
            except IndexError:
                error(f"Too many arguments provided, expected {index} reveived {len(args)}")
                quit() #? never actually reached
            if type_string.startswith("multiple:"):
                new_type = self.get_type(type_string[9:])
                new_multiple = []
                for inner_arg in args[index:]:
                    try:
                        new_multiple.append(new_type(inner_arg))
                    except TypeError:
                        error(f"Cannot convert '{inner_arg}' to required type '{new_type.__name__}'") #type:ignore
                new_args.append(new_multiple)
                break
            else:
                new_type = self.get_type(type_string)
                try:
                    if new_type == int: #? only used for flags, so if it's present it is true
                        new_args.append(True)
                    else:
                        new_args.append(new_type(arg))
                except (TypeError, ValueError):
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
        return "" #? never actually reached

    def get_help_details(self, command_name: str) -> Dict:
        return self.help_dict[self.get_root_command(command_name)]

    def get_display_args(self, args: Dict[str, Dict[str, str|bool]], extra_details:bool=True) -> List[str]:
        display_args = []
        for arg_name, arg_details in args.items():
            if arg_details["required"]:
                display_args.append(f"<{arg_name}{f":{arg_details["type"].split(":")[-1]}" if extra_details else ""}>{"..." if arg_details["type"].startswith("multiple:") else ""}") #type:ignore
            else:
                display_args.append(f"\\[{arg_name}{f":{arg_details["type"].split(":")[-1]}" if (extra_details and arg_details["type"] != "flag") else ""}]{"..." if arg_details["type"].startswith("multiple:") else ""}") #type:ignore
        return display_args

    def get_help(self, command_name: str="") -> None:
        if command_name == "":
            for command_name, command_details in self.help_dict.items():
                is_deprecated = False
                if "deprecated" in command_details.keys():
                    is_deprecated = command_details["deprecated"]
                display_args = self.get_display_args(command_details["args"], extra_details=False)
                # console.print(f"[light_green]{command_name} {" ".join(display_args)}{" " if len(display_args) != 0 else ""}[/light_green]- {command_details["description_short"]}", highlight=False)
                console.print("".join([
                    f"[strike][{log_grey}]" if is_deprecated else "[light_green]",                      #? Starting, green or grey
                    f"{command_name} {" ".join(display_args)}{" " if len(display_args) != 0 else ""}",  #? Command and its arguments followed by a space
                    f"[/light_green]" if not is_deprecated else "",                                     #? Ends green if the command isn't deprecated
                    f"- {command_details["description_short"]}",                                        #? Adds the short description
                    f"[/strike] DEPRECATED[/{log_grey}]" if is_deprecated else ""                       #? Closes the grey tag if the command is deprecated
                ]), highlight=False)
        else:
            if command_name not in self.help_dict.keys():
                if command_name not in self.aliases.keys():
                    error(f"No command with name '{command_name}', run 'help' for help")
                else:
                    command_name = self.aliases[command_name]

            command_details = self.get_help_details(command_name)
            display_args = self.get_display_args(command_details["args"])
            console.print(command_name)
            console.print(f"Usage: [light_green]{command_name} {" ".join(display_args)}{" " if len(display_args) != 0 else ""}[/light_green]", highlight=False)
            console.print(f"Description: [pale_turquoise1]{command_details["description" if "description" in command_details.keys() else "description_short"]}[/pale_turquoise1]", highlight=False)
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
