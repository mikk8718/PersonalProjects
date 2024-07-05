from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class NetworkElementError(Exception):
    pass

class Match(object):
    def __init__(self, data):
        self._data = data

    @property     
    def match_data(self):
        return self._data
    
class Matches(object):
    def __init__(self, mappedData):
        self._data = list(mappedData)
    def __len__(self):
        return len(self._data)
    def __getitem__(self, index):
        if index >= len(self):
            raise IndexError
        return Match(self._data[index])

class NetworkElement(object):
    def __init__(self, url):
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            self._driver = webdriver.Chrome(options=options)
            self._driver.get(url)
            self._driver.set_window_size(1, 1)    
            self._driver.set_window_position(-10000, 0) 
            
            while True:
                try:
                    WebDriverWait(self._driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "event__more")))
                    a_element = self._driver.find_element(By.CLASS_NAME, "event__more")
                    self._driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    self._driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", a_element)
                    time.sleep(0.5)                    
                except:
                    break
        except:
            raise NetworkElementError("Failed intial response")
        
    
    def formatTime(self, s):  
        return (s[:10], s[-5:])

    @property
    def match_divs(self):
        try:
            soup = BeautifulSoup(self._driver.page_source, 'html.parser')
            divs = soup.find_all('div', class_ = 'event__match')
            print("Extracting {}".format(len(divs)))
            return Matches(map(self.fetch, divs))
        except:
            raise NetworkElementError("failed to gather matches")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exctype, excinst, exectb):
        self._driver.quit()
    
    def fetch(self, div):
        self._driver.get(div.find('a', href=True)['href'])        
        element = WebDriverWait(self._driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "duelParticipant__startTime")))
        soup = BeautifulSoup(self._driver.page_source, 'html.parser')
        date, time = self.formatTime(
                                        soup.find('div', class_ = 'duelParticipant__startTime').find('div').text.strip()
                                    )
        homeTeam = soup.find('div', class_ = 'duelParticipant__home').find('img').get('alt')
        awayTeam = soup.find('div', class_ = 'duelParticipant__away').find('img').get('alt')
        print("{} vs {} at {}".format(homeTeam, awayTeam, (date, time)))
        return (homeTeam, awayTeam, date, time)
