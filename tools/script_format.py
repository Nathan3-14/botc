import time
from typing import Dict, List, LiteralString
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import ElementNotInteractableException, NoSuchElementException
import os
from sys import argv
import json
from .common import join_path, SCRIPTS_PATH, CURRENT_PATH

def clear_directory(script_directory: str):
    for file in os.listdir(script_directory):
        if file.endswith(".pdf"):
            os.remove(join_path(script_directory, file))
    print("Old PDFs Removed")

def download_script_pdf(script_path: str, driver: WebDriver):
    driver.get("https://script.bloodontheclocktower.com/")
    driver.implicitly_wait(5)

    file_path = driver.find_element(By.ID, "fileLoader")
    file_path.send_keys(script_path)
    try:
        download_button = driver.find_element(By.CLASS_NAME, "gfSvZh")
        download_button.click()
    except NoSuchElementException:
        print("Error loading script, please retry (nosuchelement)")
        driver.close()
        quit()
    try:
        download_a4_pdf_button = driver.find_elements(By.CSS_SELECTOR, ".sc-ckVGcZ.hfoJqb")[5]
        download_a4_pdf_button.click()
    except ElementNotInteractableException:
        print("Error loading script, please retry (notinteractable)")
        driver.close()
        quit()
    time.sleep(5)
    driver.close()
    print("New Script Downloaded")

def get_meta_index(script_data: List[Dict[str, str]]) -> int:
    for index, item in enumerate(script_data):
        if item["id"] == "_meta":
            return index
    return -1

def fix_script(script_name: str):
    script_path = join_path(SCRIPTS_PATH, script_name, f"{script_name}.json")
    script_data = json.load(open(script_path, "r"))
    meta_index = get_meta_index(script_data)
    if meta_index == -1:
        script_data.append({"id": "_meta", "name": script_name.replace("_", " ")})
    else:
        script_data[meta_index]["name"] = script_data[meta_index]["name"].lower().replace("_", " ")
    json.dump(script_data, open(script_path, "w"))
    print("Script Fixed")

def rename_script(script_path: str):
    script_directory = join_path(script_path, "..")
    old_pdf_name = [file for file in os.listdir(script_directory) if file.endswith(".pdf")][0]
    old_pdf_path = join_path(script_directory, old_pdf_name)
    new_pdf_path = join_path(script_directory, old_pdf_name.replace(" ", "_"))
    os.rename(old_pdf_path, new_pdf_path)
    print("New Script Renamed")
    
def format(script_name: str):
    current_script_directory = os.path.join(SCRIPTS_PATH, script_name)
    current_script_file = f"{script_name}.json"
    current_script_path = os.path.join(current_script_directory, current_script_file)
    if not os.path.exists(current_script_path):
        print(f"File '{current_script_path}' does not exist")
        quit()
    
    fix_script(script_name)
    clear_directory(current_script_directory)
    
    options = Options()
    options.set_preference("browser.download.folderList", 2)
    options.set_preference("browser.download.dir", current_script_directory)
    options.set_preference("pdfjs.disabled", True)
    
    download_script_pdf(current_script_path, webdriver.Firefox(options=options))
    rename_script(current_script_path)

    
if __name__ == "__main__":
    args = argv[1:]
    if len(args) != 1:
        print("Invalid args")
        quit()
    
    format(args[0])
