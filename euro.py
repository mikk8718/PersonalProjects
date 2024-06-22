from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv

def formatDate(s):  
    return (s[:10], s[-5:])

def formatEntry(homeTeam, awayTeam, date):
    return ["{} vs {}".format(homeTeam, awayTeam), date[0], date[1], date[0], date[1], "FALSE", "", ""]

url = input("enter a flashscore link with the coming fixtures: ")

options = webdriver.SafariOptions()
driver = webdriver.Safari(options=options)

driver.get(url)
html_content = driver.page_source

soup = BeautifulSoup(html_content, 'html.parser')
sportNameDivs = soup.find_all('div', class_ = 'event__match')

if sportNameDivs:
    print("Parsing matches")


with open('output.csv', mode='w', newline='') as file:
    header = ['Subject', 'Start Date', 'Start Time', 'End Date', 'End Time', 
              'All Day Event', 'Description', 'Location', 'Private']
    writer = csv.writer(file)
    writer.writerow(header)

    n = 1
    size = len(sportNameDivs)
    
    for matches in sportNameDivs:
        driver.get(matches.find('a', href=True)['href'])
        wait = WebDriverWait(driver, 10)

        element = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "duelParticipant__startTime")))
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')
        date = soup.find('div', class_ = 'duelParticipant__startTime').find('div').text.strip()
        homeTeam = soup.find('div', class_ = 'duelParticipant__home').find('img').get('alt')
        awayTeam = soup.find('div', class_ = 'duelParticipant__away').find('img').get('alt')
        writer.writerow(formatEntry(homeTeam, awayTeam, formatDate(date)))
        print("{} / {}: {} vs {}".format(n, size, homeTeam, awayTeam))
        n = n + 1

driver.quit()
print("Finished")