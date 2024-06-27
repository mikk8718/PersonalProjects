from selenium import webdriver
from bs4 import BeautifulSoup
from simple_term_menu import TerminalMenu
import subprocess

url_category = "https://www.twitch.tv/directory/category/"
url_base = "https://twitch.tv/"
options = webdriver.SafariOptions()
driver = webdriver.Safari(options=options)

categories = ["Tekken-8", "League-of-legends"]
terminal_menu = TerminalMenu(categories, title="Categories")
menu_entry_index = terminal_menu.show()


driver.get(url_category+categories[menu_entry_index].lower())
html_content = driver.page_source

soup = BeautifulSoup(html_content, 'html.parser')
container = soup.find('div', class_='ScTower-sc-1sjzzes-0 fwymPs tw-tower')
loadedStreamDivs = container.find_all('div', attrs={'data-target': True})

channels = [div.find('a', href=True)['href'] for div in loadedStreamDivs]

terminal_menu = TerminalMenu(channels, title="Channels")
menu_entry_index = terminal_menu.show()
#for div in loadedStreamDivs:
 #   channel = div.find('a', href=True)
  #  title = channel['aria-label']
   # link = channel['href']
    #driver.get(url_base+link.lower())
    #viewerCount = BeautifulSoup(driver.page_source, 'html.parser').find('span', class_="ScAnimatedNumber-sc-1iib0w9-0 hERoTc")
    #print("title: {} Viewers {}".format(title, 1))

driver.quit()
command = ["streamlink", url_base+channels[menu_entry_index].strip(), "best"]
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
process.wait()
