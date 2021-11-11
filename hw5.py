from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, ElementClickInterceptedException
from pymongo import MongoClient
import time

client = MongoClient('localhost', 27017)
chrome_options = Options()
chrome_options.add_argument('start-maximized')

driver = webdriver.Chrome('chromedriver.exe', options=chrome_options)
driver.get('https://www.mvideo.ru/')
driver.execute_script("window.scrollTo(0, 1600)")

wait = WebDriverWait(driver, 10)
button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                '//mvid-shelf-group/mvid-switch-shelf-tab-selector/mvid-carousel//button[2]')))
button.click()


while True:
    try:
        wait = WebDriverWait(driver, 10)
        button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                        '//mvid-shelf-group/mvid-carousel//button[2]')))
        button.click()
    except(TimeoutException, ElementNotInteractableException):
        break

url = '//mvid-shelf-group/mvid-carousel/div[1]/div/mvid-product-cards-group//div[@class="product-mini-card__name ng-star-inserted"]'
names = driver.find_elements(By.XPATH, url)
try:
    for name in names:
        name_list=[]
        n= name.text
        name_list.append(n)
        print(name_list)
except(ElementClickInterceptedException):
    print('Попробуйте еще разок')


url2 = '//mvid-shelf-group/mvid-carousel/div[1]/div/mvid-product-cards-group//div[@class="product-mini-card__name ng-star-inserted"]//a'
links = driver.find_elements(By.XPATH, url2)
try:
    for link in links:
        link_list=[]
        l = link.get_attribute('href')
        link_list.append(l)
        print(link_list)
except(ElementClickInterceptedException):
    print('Попробуйте еще разок')


dictionary = dict(zip(name_list, link_list))
print(dictionary)

my_dict = {name_list[i]:link_list[i] for i in range (0, len(name_list), 1)}
print(my_dict)

db = client['mvideo']
products = db['products']
products.insert_one(dictionary)


