from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import paho.mqtt.client as mqtt
import logging
from time import sleep
import sys
import shutil

from logger import (
    LogLevels,
    Logger
)
from AlphaEssMonitor import AlphaEssMonitor


logLevelMap = {
    "trace": LogLevels["Trace"],
    "debug": LogLevels["Debug"],
    "info": LogLevels["Info"],
    "notice": LogLevels["Notice"],
    "warning": LogLevels["Warning"],
    "error": LogLevels["Error"],
    "fatal": LogLevels["Fatal"],
}

if __name__ == '__main__':
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.binary_location = shutil.which("chromium-browser")
    driver = webdriver.Chrome(options=chrome_options, executable_path=shutil.which("chromedriver"))

    user_name = sys.argv[1]
    password = sys.argv[2]
    mqtt_host = sys.argv[3]
    mqtt_port = int(sys.argv[4])
    mqtt_username = sys.argv[5]
    mqtt_password = sys.argv[6]
    base_topic = sys.argv[7]
    timeout = int(sys.argv[8])
    selectedLogLevel = logLevelMap[sys.argv[9]]

    logger = Logger(selectedLogLevel)

    monitor = AlphaEssMonitor(user_name, password)
    monitor.start(driver)
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(mqtt_username, mqtt_password)
    mqtt_client.connect(host=mqtt_host, port=mqtt_port)
    mqtt_client.loop_start()

    user_name = None
    password = None
    mqtt_password = None
    mqtt_username = None

    while True:
        monitor_data = monitor.get_data()
        if monitor_data["load"] and monitor_data["load"] == 0:
            for key in monitor_data:
                logger.log_debug("Monitor data key: %s" % key)
                mqtt_client.publish(base_topic + "/" + key, monitor_data[key])
        logger.log_debug("Waiting %d seconds" % timeout)
        sleep(timeout)
