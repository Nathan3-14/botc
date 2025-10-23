import os
import pdf2image
from .common import join_path, SCRIPTS_PATH, error, console, config

success_green = config.colours["success_green"]

def image_script(script_name: str) -> None:
    current_script_directory = os.path.join(SCRIPTS_PATH, script_name)
    current_script_file = f"{script_name}.pdf"
    current_script_path = join_path(current_script_directory, current_script_file)
    if not os.path.exists(current_script_path):
        error(f"File '{current_script_path}' does not exist")
    save_path = ".".join(current_script_path.split(".")[:-1]) + ".png"
    pdf2image.convert_from_path(current_script_path, 600)[0].save(save_path)
    console.print(f"[{success_green}]Image successfully created[/{success_green}]")
    