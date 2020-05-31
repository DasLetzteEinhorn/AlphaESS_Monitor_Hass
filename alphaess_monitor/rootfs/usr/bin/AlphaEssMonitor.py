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
        self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(2) .el-input__inner").send_keys(self.user_name)
        self.driver.find_element(By.CSS_SELECTOR, ".el-form-item:nth-child(3) .el-input__inner").send_keys(self.password)
        self.driver.find_element(By.CSS_SELECTOR, ".el-button--primary").click()
        self.user_name = None
        self.password = None

    def stop(self):
        self.driver.get(self.host + "/Account/Logout")
        self.driver.quit()
        self.driver = None
        self.started = False

    def get_data(self):
        pvchartcontainerId = '1'
        loadchartcontainerId = '2'
        batterychartcontainerId = '3'
        feedinchartcontainerId = '4'
        gridchartcontainerId = '5'

        self.driver.refresh()
        WebDriverWait(self.driver, 15000).until(
            expected_conditions.visibility_of_element_located((By.ID, "tab-2")))
        sleep(10)
        self.driver.find_element(By.ID, "tab-2").click()
        sleep(10)

        return {
            'pv': self.get_value(pvchartcontainerId),
            'load': self.get_value(loadchartcontainerId),
            'battery': self.get_value(batterychartcontainerId),
            'feed_in': self.get_value(feedinchartcontainerId),
            'grid_consumption': self.get_value(gridchartcontainerId)
        }

    def get_value(self, id):
        WebDriverWait(self.driver, 5000).until(
            expected_conditions.presence_of_element_located((By.CSS_SELECTOR, ".pie-data-container > :nth-child("+id+") tspan")))
        sleep(2)
        return float(re.sub("%|kW", "", self.driver.find_element_by_css_selector(".pie-data-container > :nth-child("+id+") tspan").text))
