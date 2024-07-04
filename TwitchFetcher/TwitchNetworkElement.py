from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from enum import Enum
from simple_term_menu import TerminalMenu


class NetworkElementError(Exception):
    pass

class StreamLinkError(Exception):
    pass    

class SearchType(Enum):
    HIGH_TO_LOW = "?sort=VIEWER_COUNT"
    LOW_TO_HIGH = "?sort=VIEWER_COUNT_ASC"

class Streams(object):
    def __init__(self, mappedData):
        self.data = list(mappedData)
    def __len__(self):
        return len(list(self.data))
    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError
        return Stream(self.data[index])
    
    @property
    def format(self):
        l = self.data
        l.insert(0, "Search")
        return l

class TwitchNetworkElement(object):    
    def __init__(self, url, searchType):
        try:
            self.searchType = searchType
            self.driver = webdriver.Chrome()
            self.driver.get(url+self.searchType.value)
            self.driver.set_window_size(10, 10)    
            self.driver.set_window_position(-10000, 0)
        except:
            raise NetworkElementError("Failed intial response")
        
    def __enter__(self):
        return self
    
    def __exit__(self, exctype, excinst, exectb):
        self.driver.quit()
        
    @property
    def streamers(self):
        try:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            time.sleep(0.5)
            container = soup.find('div', class_='ScTower-sc-1sjzzes-0 fwymPs tw-tower')
            loadedStreamDivs = container.find_all('div', attrs={'data-target': True})
            return Streams(map(lambda div: div.find('a', href=True)['href'], loadedStreamDivs))
        except:
            raise NetworkElementError("Can't load category")

class Stream(object):
    def __init__(self, data):
        self.data = data
        self.isFavorite = False

    @property
    def handle(self):
        return self.data
    
class MenuError(Exception):
    pass

class Menu(object):
    def __init__(self, options, title, twe):
        try:
            self.twe = twe
            self.menu = TerminalMenu(options, title=title)
            self.index = self.menu.show()
            self.validate_index(self.index)
        except:
            raise MenuError("Couldn't load menu")    
    
    def __enter__(self):
        return self
    
    def __exit__(self, exctype, excinst, exectb):
        pass
    
    @property
    def target_streamer(self):
        if not hasattr(self, 'handle'):
            raise MenuError("Error")
        return "https://www.twitch.tv" + getattr(self, 'handle')
    
    def validate_index(self, index):
        if not isinstance(self.index, int):
            raise MenuError("Index not loaded properly")
        if self.index < 0:
            raise MenuError("Can't use index")
        if self.index == 0:
            setattr(self, 'handle', "/" + input("Search streamer: "))
        else:
            setattr(self, 'handle', self.twe.streamers[self.index].handle)