# -*- coding: utf-8 -*-

from selenium.webdriver.common.by import By

class Base:

    def __init__(self, driver):
        self.driver = driver
    
    def navigate_to(self, url):
        if url.startswith("http"):
            self.driver.get(url)
        else:
            self.driver.get(cfg['base_url'] + url)
