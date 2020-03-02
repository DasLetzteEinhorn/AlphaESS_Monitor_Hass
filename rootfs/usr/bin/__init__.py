from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.chrome.options import Options
import paho.mqtt.client as mqtt
from bash_io_logger import BashIoLogger
from time import sleep
import re
import sys
import shutil

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


if __name__ == '__main__':
    logger = BashIoLogger()

    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.binary_location = shutil.which("chromium-browser")
    driver = webdriver.Chrome(options=chrome_options, executable_path=shutil.which("chromedriver"))

    user_name = sys.argv[1]
    password = sys.argv[2]
    mqtt_host = sys.argv[3]
    mqtt_username = sys.argv[4]
    mqtt_password = sys.argv[5]
    base_topic = sys.argv[6]
    timeout = int(sys.argv[7])

    monitor = AlphaEssMonitor(user_name, password)
    monitor.start(driver)
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(mqtt_username, mqtt_password)
    mqtt_client.connect(mqtt_host)
    mqtt_client.loop_start()

    user_name = None
    password = None
    mqtt_password = None
    mqtt_username = None

    while True:
        monitor_data = monitor.get_data()
        for key in monitor_data:
            logger.log_debug("Monitor data key:" + key)
            mqtt_client.publish(base_topic + "/" + key, monitor_data[key])
        logger.log_debug("Waiting " + str(timeout) + " seconds")
        sleep(timeout)
