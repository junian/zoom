#!/usr/bin/env python

# Starting of the program
############## ! Imports ##############
# ? Selenium --> For interacting with the web browser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
# from pynput.keyboard import Key, Controller
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import time
import names
import random

# ? Time --> For pausing the program
from time import sleep

# ? Questionary --> For beautiful command line prompts
from questionary import Style, select, text


# ? OS --> For clearing the screen
from os import system, name as OSNAME

# ? Rich --> For a box and loading bar
from rich import print
from rich.console import Console

# keyboard = Controller()
globalId = ""
globalPassword = ""

console = Console()
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    TextColumn,
)
from rich.align import Align

def is_null_or_whitespace(s):
    return s is None or s.strip() == ''

############## ! Functions ##############
# * Initializing selenium with Chrome settings
def setSelenium():
    global allNames, chromeOptions

    chromeOptions = ChromeOptions()
    chromeOptions.add_argument("--headless=new")
    chromeOptions.add_argument('--no-sandbox')
    chromeOptions.add_experimental_option("detach", True)
    chromeOptions.add_argument("--use-fake-ui-for-media-stream")
    prefs = {"profile.managed_default_content_settings.images": 2}
    chromeOptions.add_experimental_option("prefs", prefs)
    # ? Reading all the names from 'names.txt'
    allNames = open("names.txt", "r").read().split("\n")
    random.shuffle(allNames)


# * Clicking join from browser on the page
def clickJoinFromBrowser(driver):
    try:
        # Locate the "Join from Your Browser" link and click it
        join_from_browser_link = driver.find_element(By.LINK_TEXT, "Join from Your Browser")
        join_from_browser_link.click()
    except Exception as e:
        print("Error handling Zoom prompt:", str(e))


# * Function if user selected ID and Password method
def idPass(id=None, password=None):
    global globalId, globalPassword

    # ? If ID is not provided
    if id == None:
        id = text("Enter Zoom Meeting ID:", style=minimalStyle).ask().replace(' ', '')

    else:
        # ? If ID is provided
        id = int(str(id.replace(" ", "")))
    
    globalId = id

    # ? If password is not provided
    if password == None:
        password = text("Enter Zoom Meeting Password:", style=minimalStyle).ask()

    answer = text("Enter Number of Zoom Meeting Participants:", style=minimalStyle).ask()
    numberOfParticipants = int(answer)

    globalPassword = password

    # Define the maximum number of threads
    max_threads = 16

    # Use a ThreadPoolExecutor to manage the threads
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
        # Map the process_data function to the data_list
        results = list(executor.map(process_data, allNames[:numberOfParticipants]))

    print("All threads have finished processing.")

def process_data(name):
    if is_null_or_whitespace(name):
        return
    
    driver = webdriver.Chrome(options=chromeOptions)

    try:
        # ? Opening the website
        targetUrl=f"https://app.zoom.us/wc/{globalId}/join?from=pwa"
        print(targetUrl)
        driver.get(targetUrl)
        sleep(0.25)
            #driver.switch_to.frame(driver.find_element(By.TAG_NAME,"iframe"))
        # ? Entering password
        pwd = driver.find_element(By.ID, "input-for-pwd")
        pwd.clear()
        pwd.send_keys(globalPassword)
        
        # ? Entering name
        user = driver.find_element(By.ID, "input-for-name")
        user.clear()
        user.send_keys(name)

        # ? Joining audio and muting mic
        audioButton = driver.find_element(By.ID, "preview-audio-control-button")
        audioButton.click()
        sleep(0.1)
        audioButton2 = driver.find_element(By.ID, "preview-audio-control-button")
        audioButton2.click()
        sleep(0.1)
        audioButton2 = driver.find_element(By.ID, "preview-audio-control-button")
        audioButton2.click()
        user.send_keys(Keys.RETURN)
        sleep(0.1)
    except Exception as e:
        print("Error handling Zoom prompt:", str(e))
        driver.quit()
        return None
    
    return driver





# * Function if user selected link method
def link(link="https://learn.zoom.us/j/94950913565?pwd=LzhoOVdybFBKVWVwOU9za3Ywd01SQT09#success"):
    # ? If link is not provided
    if link == None:
        link = text("Enter Zoom Meeting Link:", style=minimalStyle).ask() + "#success"

    # ? Creating a loop for all the names provided
    for name in allNames:
        # ? Opening the browser
        
        driver = webdriver.Chrome(options=chromeOptions)

        # ? Opening the website
        driver.get(link)

        sleep(5)

        # Dismiss the alert (click "Cancel")



        driver.execute_script("document.getElementsByClassName('mbTuDeF1')[0].click();")
        # keyboard.press_and_release('enter')
        driver.execute_script("document.getElementsByTagName('a')[6].click();")





   

        sleep(5)

        driver.switch_to.frame(driver.find_element(By.TAG_NAME,"iframe"))

        print(name)
        WebDriverWait(driver, 1000).until(EC.presence_of_element_located((By.CLASS_NAME, "preview-meeting-info-field-input")) )
        user = driver.find_element(By.CLASS_NAME, "preview-meeting-info-field-input")
        user.clear()
        user.send_keys(name)

        # ? Joining audio and muting mic
        audioButton = driver.find_element(By.ID, "preview-audio-control-button")
        audioButton.click()
        sleep(0.1)
        audioButton2 = driver.find_element(By.ID, "preview-audio-control-button")
        audioButton2.click()
        user.send_keys(Keys.RETURN)


# * Loading Bar
def StatBar(time: float, desc: str):
    progress_bar = Progress(
        TextColumn(f"{desc} "),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
    )
    with progress_bar as p:
        for i in p.track(range(100), description=desc):
            sleep(time / 1000)
    sleep(0.5)


############## ! Printing Options ##############
if __name__ == "__main__":
    setSelenium()
    system("clear" if OSNAME == 'posix' else "cls")
    Align.center(
        StatBar(2, desc="[cyan]Loading Zoom Bomber"), vertical="middle"
    )
    system("clear" if OSNAME == 'posix' else "cls")
    console.print(
        Panel.fit("[bold italic #77DDD4]Zoom Bomber", padding=(0, 22))
    )
    minimalStyle = Style(
        [
            ("answer", "fg:#FFFFFF italic"),  # ? White
            ("question", "fg:#FFFFFF bold"),  # ? White
            ("pointer", "fg:#00FFFF bold"),  # ? Cyan
            ("highlighted", "fg:#FFFFFF"),  # ? White
            ("selected", "fg:#A9A9A9"),  # ? Grey
            ("qmark", "fg:#77DD77"),  # ? Green
        ]
    )
    userSelect = select(
        "Choose a way to bomb your meetings: ", ["ID/Pass", "Link"], style=minimalStyle
    ).ask()
    sleep(0.5)
    system("clear" if OSNAME == 'posix' else "cls")
    if userSelect == "ID/Pass":
        idPass()
    elif userSelect == "Link":
        link()
    else:
        print("Unknown error, please restart the program")
