import json
from tabnanny import check
from typing import List
import cli
from sys import argv
import tools

# def add(number_1: int, number_2: int) -> None:
#     print(number_1+number_2)

# def subtract(number_1: int, number_2: int) -> None:
#     print(number_1-number_2)

# def _sum(numbers: List[int]) -> None:
#     total = 0
#     for number in numbers:
#         total += number
#     print(total)

# def hello(name: str="") -> None:
#     if name == "":
#         print("Hello!")
#     else:
#         print(f"Hello {name}!")

# executor = cli.Executor(json.load(open("test/test_help_dict.json", "r")), {
#     "add": add,
#     "subtract": subtract,
#     "hello": hello,
#     "sum": _sum
# })
# executor.run_from_command_line(argv[1:])


executor = cli.Executor(json.load(open("tools/help_dict.json", "r")), {
    "search": tools.display_search,
    "list": tools.list_script,
    "format": tools.format,
    "check": tools.check,
    "download": tools.download
})
print(argv[1:])
executor.run_from_command_line(argv[1:])
