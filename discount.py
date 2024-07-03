from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



url = 'https://minetilbud.dk/tilbudsaviser/netto/1'
options = webdriver.SafariOptions()
driver = webdriver.Safari(options=options)
driver.set_window_size(500, 500)


#/html/body/div[3]/div[2]/div[1]/div/div/div/div[2]/div/div[3]/div
driver.get(url)
html_content = driver.page_source
soup = BeautifulSoup(html_content, 'html.parser')

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "unselectable done")))
#a_element = driver.find_element(By.CLASS_NAME, "unselectable done")   

time.sleep(1)
#a_element = driver.find_element(By.XPATH, "//*[@id=Layer_1]")   
container = soup.find('div', class_='unselectable done')
discounts = container.find_all('div', class_='pw book-spread')
print(len(discounts))

#a_element.click()



time.sleep(2)
driver.quit()