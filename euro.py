from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
from selenium.webdriver.common.action_chains import ActionChains


def formatDate(s):  
    return (s[:10], s[-5:])

def formatEntry(homeTeam, awayTeam, date):
    return ["{} vs {}".format(homeTeam, awayTeam), date[0], date[1], date[0], date[1], "FALSE", "", ""]


url = input("enter a flashscore link with the coming fixtures: ")

    
#url = "https://www.flashscore.com/football/england/premier-league/fixtures/"
options = webdriver.SafariOptions()
driver = webdriver.Safari(options=options)

driver.get(url)
html_content = driver.page_source

#a_element = driver.find_element(By.CLASS_NAME, "event__more")
#driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", a_element)
#time.sleep(1)

soup = BeautifulSoup(html_content, 'html.parser')

# TODO
# fix view more (done)
# add try catch (done)
# more robust input handling
controller = True


with open('output.csv', mode='w', newline='') as file:
    header = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 
              'All Day Event', 'Description', 'Location', 'Private']
    writer = csv.writer(file)
    writer.writerow(header)

    n = 1    
    while controller:
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "event__more")))
            a_element = driver.find_element(By.CLASS_NAME, "event__more")   
            driver.execute_script("arguments[0].scrollIntoView(true); arguments[0].click();", a_element)
            time.sleep(2)
            print("error")
        except:
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            sportNameDivs = soup.find_all('div', class_ = 'event__match')
            
            size = len(sportNameDivs)

            for matches in sportNameDivs:
                driver.get(matches.find('a', href=True)['href'])
                wait = WebDriverWait(driver, 10)

                element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "duelParticipant__startTime")))
                html_content = driver.page_source
                soup = BeautifulSoup(html_content, 'html.parser')
                date = soup.find('div', class_ = 'duelParticipant__startTime').find('div').text.strip()
                homeTeam = soup.find('div', class_ = 'duelParticipant__home').find('img').get('alt')
                awayTeam = soup.find('div', class_ = 'duelParticipant__away').find('img').get('alt')
                writer.writerow(formatEntry(homeTeam, awayTeam, formatDate(date)))
                print("{} / {}: {} vs {}".format(n, size, homeTeam, awayTeam))
                n = n + 1
                time.sleep(1)
            controller = False

driver.quit()
print("Finished")