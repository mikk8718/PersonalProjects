from selenium import webdriver
from bs4 import BeautifulSoup
import time
from simple_term_menu import TerminalMenu
import sys

class NetworkElementError(Exception):
    pass

class MenuError(Exception):
    pass

class Article(object):
    def __init__(self, data):
        self.data = data
        
    @property     
    def title(self):
        return self.data['title']
    
    @property
    def link(self):
        return "https://www.flashscore.dk"+self.data['href']
    
class Articles(object):
    def __init__(self, data):
        self._data = data
    def __len__(self):
        return len(self._data)
    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError
        return Article(self._data[index])
    
    @property
    def titles(self):
        return list(map(lambda x: x['title'], self._data))

class NetworkElement(object):
    def __init__(self, url):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            self.driver = webdriver.Chrome(options=options)
            self.driver.get(url)
            self.driver.set_window_size(1500, 1500)    
        except:
            raise NetworkElementError("Failed intial response")

    @property
    def articles(self):
        try:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            news_sections = soup.find_all('div', class_='fsNewsSection fsNewsSection__mostRecent fsNewsSection__noTopped')
            return Articles((news_sections[0].find_all('a') + news_sections[1].find_all('a'))[:-1])
        except:
            raise NetworkElementError("Failed to gather news")
        
    def __enter__(self):
        return self
    
    def __exit__(self, exctype, excinst, exectb):
        self.driver.quit()

class Menu(object):
    def __init__(self, options, title):
        try:
            self.menu = TerminalMenu(options, title=title, multi_select=True)
            self.index = self.menu.show()
        except:
            raise MenuError("Couldn't load menu")    
    
    def __enter__(self):
        return self
    
    def __exit__(self, exctype, excinst, exectb):
        sys.exit()
