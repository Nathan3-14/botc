from typing import Any, Callable, Dict
from .help import Help
from .common import console

class Executor:
    def __init__(self, help_dict: Dict[str, Any], command_dict: Dict[str, Callable]) -> None:
        self.help = Help(help_dict)
        self.command_dict = command_dict | {"help": self.help.get_help}
    
    def run(self, _input: str) -> None:
        input_split = _input.split(" ")
        command_name = input_split[0]
        command_args = input_split[1:] if len(input_split) > 1 else []
        self.command_dict[self.help.get_root_command(command_name)](*self.help.convert_types(command_name, command_args))
        