import json
from tabnanny import check
from typing import List
import cli
from sys import argv
import tools


executor = cli.Executor(json.load(open("tools/help_dict.json", "r")), {
    "search": tools.display_search,
    "list": tools.list_script,
    "format": tools.format,
    "check": tools.check,
    "download": tools.download
})
print(argv[1:])
executor.run_from_command_line(argv[1:])
