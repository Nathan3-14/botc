import json
import cli
from sys import argv
import tools


executor = cli.Executor(json.load(open("tools/help_dict.json", "r")), {
    "search": tools.display_search,
    "display": tools.display_script,
    "format": tools.format_script,
    "download": tools.download_script,
    "upload": tools.upload_script,
    "image": tools.image_script,
    "select": tools.select_scripts,
    "sets": tools.get_script_sets
})
executor.run_from_command_line(argv[1:])
