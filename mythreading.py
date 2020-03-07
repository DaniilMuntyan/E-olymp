from multiprocessing.sharedctypes import synchronized
from threading import Thread
import os
from selenium.webdriver.support.wait import WebDriverWait
import json
from solution import Solution
from solutionencoder import SolEncoder


class MyThread(Thread):

    def __init__(self, name, driver, list, path, comps, beg, end):
        Thread.__init__(self)
        self.name = name
        self.driver = driver
        self.list = list
        self.path = path
        self.comps = comps
        self.beg = beg
        self.end = end

    def run(self):
        driver = self.driver
        list = self.list
        beg = self.beg
        end = self.end
        path = self.path
        comps = self.comps
        for temp in list[beg:end]:
            driver.get('https://www.e-olymp.com' + temp)
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name('text-muted'))
            send_date = driver.find_element_by_xpath('//table/tbody/tr[1]/td[2]').text
            driver.find_element_by_xpath('//table/tbody/tr[1]/td[1]/a').click()
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name('eo-pie__overlay'))
            name = driver.find_element_by_xpath("//div[@id='react-content']/div/div[1]/div/div[1]/a").text
            compiler = driver.find_element_by_xpath("//div[@id='react-content']/div/div[1]/div/div[3]/div").text
            time = float(driver.find_element_by_xpath('//tfoot/tr/td[3]/span[4]').text.replace(',', '.'))
            memory = int(driver.find_element_by_xpath('//tfoot/tr/td[4]/span[4]').text.replace(' ', ''))
            code = driver.find_element_by_tag_name('code').text
            path += str(list.index(temp) + 1) + ' ' + name
            print(json.dumps(Solution(name, compiler, send_date, time, memory, code), cls=SolEncoder))
            #print(Solution(name, compiler, send_date, time, memory, code).toJSON())
            try:
                os.makedirs(path)
                file = open(path + '/' + name + comps[compiler], 'w')
                file.write(code)
                file.close()
            except OSError or IOError or BaseException:
                print("Error\n" + path)

            path = self.path



