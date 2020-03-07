from datetime import datetime
import os
import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import requests
from solution import Solution
from mythreading import MyThread
from bs4 import BeautifulSoup
from threading import Thread


def sign_in(login, password, base_url):
    driver = webdriver.Opera(executable_path=r'D:\Python\Парсинг\Eolymp\operadriver.exe')
    driver.get(base_url)
    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('username'))
    driver.find_element_by_id('username').send_keys(login)
    driver.find_element_by_id('password').send_keys(password)
    driver.find_element_by_xpath("//input[@type='submit']").click()
    #WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('username'))
    return driver


def main_function():
    base_url = r'https://www.e-olymp.com/ru/login'
    url = r'https://www.e-olymp.com/ru/users/muntyan/punchcard'

    # options = webdriver.ChromeOptions()
    # options.add_argument("user-data-dir=" + "C:\Users\Админ\AppData\Local\Google\Chrome\User Data")
    # driver = webdriver.Chrome(executable_path='D:\chromedriver_win32\chromedriver.exe', options=options)
    # driver.get(url)

    opera_profile = r'C:\Users\Админ\AppData\Roaming\Opera Software\Opera Stable'
    options = webdriver.ChromeOptions()
    options.add_argument('user-data-dir=' + opera_profile)
    options._binary_location = r'C:\Program Files (x86)\Opera\66.0.3515.72\opera.exe'
    driver = webdriver.Opera(executable_path=r'D:\Python\Парсинг\Eolymp\operadriver.exe', options=options)

    driver.get(url)

    '''wait = WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('username'))
    driver.find_element_by_id('username').send_keys('login')
    driver.find_element_by_id('password').send_keys('password')
    driver.find_element_by_xpath("//input[@type='submit']").click()
    driver.get(url)'''

    WebDriverWait(driver, 10).until(lambda x: x.find_element_by_id('punch-card'))

    #page = requests.get(url)
    c = 0
    list = []

    bstime = datetime.now()
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for i in soup.find(id='punch-card').find_all(lambda tag: tag.name == 'a' and
                                                 '100%' in tag.get('title')):
        c += 1
        list.append(i.get('href'))

    print(datetime.now() - bstime)

    path = "D:/Python/E-olymp/"

    comps = {'Judge C++': '.cpp', 'Judge Python': '.py', 'Judge Pascal': '.p', 'Judge Java': '.java'}

    drivers = [driver]

    n = 2
    part = int(len(list) / n)

    for i in range(0, (n - 1)):
        drivers.append(sign_in('muntyan', 'Wusu0813', base_url))

    k = 0
    i = 0
    print("part = " + str(part))

    while k < len(list):
        if k + 2*part > len(list):
            ithread = MyThread(str(i+1), drivers[i], list, path, comps, k, len(list))
            k += part
        else:
            ithread = MyThread(str(i+1), drivers[i], list, path, comps, k, k + part)
        k += part
        i += 1
        ithread.start()


if __name__ == "__main__":
    main_function()



