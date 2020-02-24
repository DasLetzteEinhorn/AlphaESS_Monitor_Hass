from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
from time import sleep
import re

from const import (
    DEFAULT_HOST
)

user_name = ""
password = ""

class AlphaEssMonitor():
    def __init__(self, user_name, password, host = DEFAULT_HOST):
        self.user_name = user_name
        self.password = password
        self.host = host
        self.started = False

    def start(self, driver):
        if self.started:
            return

        self.driver = driver

        self.started = True
        self.driver.get(self.host)
        self.driver.set_window_size(968, 1030)
        self.driver.find_element(By.ID, "txtUserName").send_keys(self.user_name)
        self.driver.find_element(By.ID, "txtUserPWD").send_keys(self.password)
        self.driver.find_element(By.ID, "Login").click()
        
        self.vars = {}
    
    def stop(self):
        self.driver.get(self.host + "/Account/Logout")
        self.driver.quit()
        self.driver = None
        self.started = False
    
    def get_data(self):
        pvchartcontainerId = 'pvchartcontainer'
        loadchartcontainerId = 'loadchartcontainer'
        batterychartcontainerId = 'batterychartcontainer'
        feedinchartcontainerId = 'feedinchartcontainer'
        gridchartcontainerId = 'gridchartcontainer'

        self.driver.refresh()
        WebDriverWait(self.driver, 5000).until(expected_conditions.visibility_of_element_located((By.LINK_TEXT, "Power Diagram")))
        sleep(5)
        self.driver.find_element(By.LINK_TEXT, "Power Diagram").click()
        
        return {
            'pvchartcontainer': self.get_value(pvchartcontainerId),
            'loadchartcontainer': self.get_value(loadchartcontainerId),
            'batterychartcontainer': self.get_value(batterychartcontainerId),
            'feedinchartcontainer': self.get_value(feedinchartcontainerId),
            'gridchartcontainer': self.get_value(gridchartcontainerId)
        }
    
    def get_value(self, id):
        WebDriverWait(self.driver, 5000).until(expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#"+id+" span")))
        sleep(0.1)
        return float(re.sub("%|kW", "", self.driver.find_element_by_css_selector("#"+id+" span").text))



options = Options()
#options.headless = True
options.binary_location=r"C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
driver = webdriver.Chrome(chrome_options=options, executable_path="./chromedriver.exe")

monitor = AlphaEssMonitor(user_name, password)
monitor.start(driver)

print(monitor.get_data())

monitor.stop()