import json
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
    user_name = sys.argv[1]
    password = sys.argv[2]
    mqtt_host = sys.argv[3]
    mqtt_port = int(sys.argv[4])
    mqtt_username = sys.argv[5]
    mqtt_password = sys.argv[6]
    base_topic = sys.argv[7]
    timeout = int(sys.argv[8])
    selectedLogLevel = logLevelMap[sys.argv[9]]

    if sys.argv[10] == "":
        serial_numbers = []
    else:
        serial_numbers = list(map(lambda number: number.strip(), sys.argv[10].split(",")))

    print(json.dumps("".split(",")))

    logger = Logger(selectedLogLevel)
    
    logger.log_debug("logger created")
    
    monitor = AlphaEssMonitor(user_name, password, logger, serial_numbers)
    monitor.start()
    mqtt_client = mqtt.Client()
    mqtt_client.username_pw_set(mqtt_username, mqtt_password)
    mqtt_client.connect(host=mqtt_host, port=mqtt_port)
    mqtt_client.loop_start()

    user_name = None
    password = None
    mqtt_password = None
    mqtt_username = None

    logger.log_debug("start while loop")
    while True:
        monitor_data = monitor.get_data()
        for key in monitor_data:
            logger.log_debug("Monitor data key: {key}\t\t{data}".format(key = key, data = monitor_data[key]))
            mqtt_client.publish(base_topic + "/" + key, monitor_data[key])
        logger.log_debug("Waiting {timeout} seconds".format(timeout = timeout))

        sleep(timeout)
