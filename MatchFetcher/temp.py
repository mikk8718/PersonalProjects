from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

url = "https://www.flashscore.com/football/england/premier-league/fixtures/"
options = webdriver.SafariOptions()
driver = webdriver.Safari(options=options)


driver.get(url)
html_content = driver.page_source

soup = BeautifulSoup(html_content, 'html.parser')
sportNameDivs = soup.find_all('div', class_ = 'event__match')

print("before {}".format(len(sportNameDivs)))


#a_element = driver.find_element(By.CLASS_NAME, "event__more")
#driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", a_element)
#element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, 'event__more')))
#element.click()
controller = True
while controller:
    try:
        print("refreshing")
        a_element = driver.find_element(By.CLASS_NAME, "event__more")
        driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", a_element)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "event__more")))
        time.sleep(2)
    except:
        print("done")
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        sportNameDivs = soup.find_all('div', class_ = 'event__match')
        for matches in reversed(sportNameDivs):
            driver.get(matches.find('a', href=True)['href'])
            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "duelParticipant__startTime")))
            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')
            date = soup.find('div', class_ = 'duelParticipant__startTime').find('div').text.strip()
            homeTeam = soup.find('div', class_ = 'duelParticipant__home').find('img').get('alt')
            awayTeam = soup.find('div', class_ = 'duelParticipant__away').find('img').get('alt')
            #writer.writerow(formatEntry(homeTeam, awayTeam, formatDate(date)))
            print("{} / {}: {} vs {}".format(1, 1, homeTeam, awayTeam))
            time.sleep(1)
        controller = False
        print(len(sportNameDivs))
        


soup = BeautifulSoup(driver.page_source, 'html.parser')
sportNameDivs = soup.find_all('div', class_ = 'event__match')
print("after {}".format(len(sportNameDivs)))

driver.quit()