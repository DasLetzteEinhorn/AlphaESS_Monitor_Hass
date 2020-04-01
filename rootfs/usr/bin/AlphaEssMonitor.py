import re
from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from const import (
    DEFAULT_HOST
)


class AlphaEssMonitor():
    def __init__(self, user_name, password, host=DEFAULT_HOST):
        self.user_name = user_name
        self.password = password
        self.host = host
        self.started = False
        self.driver = None

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
        self.user_name = None
        self.password = None

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
        WebDriverWait(self.driver, 5000).until(
            expected_conditions.visibility_of_element_located((By.LINK_TEXT, "Power Diagram")))
        sleep(5)
        self.driver.find_element(By.LINK_TEXT, "Power Diagram").click()

        return {
            'pv': self.get_value(pvchartcontainerId),
            'load': self.get_value(loadchartcontainerId),
            'battery': self.get_value(batterychartcontainerId),
            'feed_in': self.get_value(feedinchartcontainerId),
            'grid_consumption': self.get_value(gridchartcontainerId)
        }

    def get_value(self, id):
        WebDriverWait(self.driver, 5000).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, "#" + id + " span")))
        sleep(0.1)
        return float(re.sub("%|kW", "", self.driver.find_element_by_css_selector("#" + id + " span").text))