from typing import Any, Callable, Dict, List
from .help import Help
from .common import console

class Executor:
    def __init__(self, help_dict: Dict[str, Any], command_dict: Dict[str, Callable]) -> None:
        self.help = Help(help_dict)
        self.command_dict = command_dict | {"help": self.help.get_help}
    
    def run(self, command_name: str, command_args: List[str]) -> None:
        self.command_dict[self.help.get_root_command(command_name)](*self.help.convert_types(command_name, command_args))
    
    def run_from_command_line(self, args: List[str]) -> None:
        """
        Can just be run as run_from_command_line(sys.argv)
        """
        if args[0].endswith(".py"):
            self.run(args[1], args[2:])
        else:
            self.run(args[0], args[1:])
        