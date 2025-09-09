import json
import cli
from sys import argv

def add(number_1: int, number_2: int) -> None:
    print(number_1+number_2)

def subtract(number_1: int, number_2: int) -> None:
    print(number_1-number_2)

def hello(name: str="") -> None:
    if name == "":
        print("Hello!")
    else:
        print(f"Hello {name}!")

executor = cli.Executor(json.load(open("test/test_help_dict.json", "r")), {
    "add": add,
    "subtract": subtract,
    "hello": hello
})
executor.run(" ".join(argv[1:]))
