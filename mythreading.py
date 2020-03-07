from multiprocessing.sharedctypes import synchronized
from threading import Thread
import os
from selenium.webdriver.support.wait import WebDriverWait
import json
import time as tm
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
            link = driver.current_url
            text = driver.find_element_by_xpath("//div[@class='eo-paper__content']")\
                .text
            driver.find_element_by_xpath('//table/tbody/tr[1]/td[1]/a').click()
            WebDriverWait(driver, 10).until(lambda x: x.find_element_by_class_name('eo-pie__overlay'))
            name = driver.find_element_by_xpath("//div[@id='react-content']/div/div[1]/div/div[1]/a").text
            compiler = driver.find_element_by_xpath("//div[@id='react-content']/div/div[1]/div/div[3]/div").text
            time = float(driver.find_element_by_xpath('//tfoot/tr/td[3]/span[4]').
                         text.replace(',', '.').replace(' ', ''))
            memory = int(driver.find_element_by_xpath('//tfoot/tr/td[4]/span[4]').text.replace(' ', ''))
            code = driver.find_element_by_tag_name('code').text
            sol = Solution(name, text, link, compiler, send_date, time, memory, code)
            name = MyThread.check_dir(name)
            path += str(list.index(temp) + 1) + ' ' + name
            try:
                os.makedirs(path)
                file = open(path + '/' + name + comps[compiler], 'w')
                file.write(code)
                file.close()
                with open(path + '/' + name + '.json', 'w', encoding='utf-8') as file:
                    json.dump(sol, file, cls=SolEncoder, ensure_ascii=False)
                with open(path + '/' + "Условие" + '.txt', 'w', encoding='utf-8') as file:
                    file.write(sol.text)
                    file.close()
            except OSError or IOError or BaseException as err:
                print("Error:\n", err)

            path = self.path

        driver.close()
        driver.quit()

    @staticmethod
    def check_dir(s):
        list = ["/", "\\", ':', '?', '"', "<", ">", '|']
        print('s = ' + s)
        for temp in list:
            if temp in s:
                print('temp = ' + temp)
                s = s.replace(temp, '')
        return s
