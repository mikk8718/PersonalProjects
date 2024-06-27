from selenium import webdriver
from bs4 import BeautifulSoup
from simple_term_menu import TerminalMenu
import subprocess
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains

url_category = "https://www.twitch.tv/directory/category/"
url_base = "https://twitch.tv/"
url_base_category = "https://www.twitch.tv/directory"
options = webdriver.SafariOptions()
driver = webdriver.Safari(options=options)
driver.set_window_size(1, 1)
driver.set_window_position(-2000, 0)  # Moves the window off-screen

driver.get(url_base_category)
soup = BeautifulSoup(driver.page_source, 'html.parser')

time.sleep(0.5)
container = soup.find('div', class_='ScTower-sc-1sjzzes-0 cejWni tw-tower')
loadedStreamDivs = container.find_all('div', attrs={'data-target': True})

categories = [div.find('h2', class_='CoreText-sc-1txzju1-0 gLOyjL')['title'] for div in loadedStreamDivs[::2]]
categories = [title.replace(" ", "-") for title in categories]
categories.insert(0, "Search")

terminal_menu = TerminalMenu(categories, title="Categories")
menu_entry_index = terminal_menu.show()

channels = []
if menu_entry_index is None:
    sys.exit()
elif menu_entry_index == 0:
    channels = [input("Try playing streamer: ")]
else: 
    driver.get(url_category+categories[menu_entry_index].lower())
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    time.sleep(0.5)
    container = soup.find('div', class_='ScTower-sc-1sjzzes-0 fwymPs tw-tower')
    loadedStreamDivs = container.find_all('div', attrs={'data-target': True})
    channels = [div.find('a', href=True)['href'] for div in loadedStreamDivs]
    terminal_menu = TerminalMenu(channels, title="Channels")
    menu_entry_index = terminal_menu.show()

driver.quit()
command = ["streamlink", url_base+channels[menu_entry_index], "best"]
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
process.wait()
