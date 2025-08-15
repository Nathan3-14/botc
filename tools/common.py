import os

def join_path(path: str, *paths: str):
    return os.path.normpath(os.path.join(path, *paths))

CURRENT_PATH = os.getcwd()
SCRIPTS_PATH = join_path(CURRENT_PATH, "scripts")

