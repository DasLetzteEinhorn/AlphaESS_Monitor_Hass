import re as regex
import time
import json

import requests

from const import (
    DEFAULT_HOST
)


class AlphaEssMonitor():
    def __init__(self, user_name, password, logger, serial_numbers=[], host=DEFAULT_HOST):
        self.user_name = user_name
        self.password = password
        self.host = host
        self.logger = logger
        self.serial_numbers = serial_numbers
        self.init()

    def start(self):
        self.logger.log_debug("Starting monitor")
        self.login()
        
    def stop(self):
        self.logger.log_debug("Stopping monitor")
        self.init()
        
    def init(self):
        self.expiration_time = 0
        self.auth_token = None
        self.refresh_token = None
        self.expiration_buffer = 0

    def get_data(self):
        if self.expiration_time < self.get_current_time() + self.expiration_buffer: # todo: get offset from config?
            if not self.login():
                return None

        serial_numbers = self.get_serial_numbers()

        data = {}

        for serial_number in serial_numbers:
            self.logger.log_trace("Get data for serial number " + serial_number)

            response = requests.get(self.host + "/api/ESS/GetLastPowerDataBySN?noLoading=true&sys_sn=" + serial_number, headers=self.get_headers())
            if self.handle_error_status_code(response):
                return
            data[serial_number] = json.dumps(response.json()["data"])

        return data

    def handle_error_status_code(self, response):
        self.logger.log_trace("Handle error for response. StatusCode: " + str(response.status_code) + ", Reason: " + response.text)

        status_code = response.status_code
        if status_code == 200:
            status_code = response.json()["code"]
            if status_code == 200:
                return False

        self.logger.log_error("No successful request. StatusCode: " + str(status_code) + ", Reason: " + response.text)        

        switcher = {
            401: self.handle_forbidden,
            403: self.handle_forbidden
        }

        handler = switcher.get(status_code)
        handler(response)

        return True

    def handle_forbidden(self):
        self.init()

    def get_serial_numbers(self):
        self.logger.log_trace("Try get serial numbers. Cached: " + json.dumps(self.serial_numbers))

        if self.serial_numbers is not None and len(self.serial_numbers) != 0:
            return self.serial_numbers

        serial_numbers_response = requests.get(self.host + "/api/Account/GetCustomMenuESSlist", headers=self.get_headers())

        if self.handle_error_status_code(serial_numbers_response):
            return []

        self.serial_numbers = list(map(lambda serial_number_obj: serial_number_obj["sys_sn"], serial_numbers_response.json()["data"]))
        return self.serial_numbers

    def login(self):
        if self.expiration_time > self.get_current_time():
            self.logger.log_trace("Try login with refresh token")

            refresh_data = {
                'userName': self.user_name,
                'accessToken': self.auth_token,
                'refreshTokenKey': self.refresh_token
            }
            login_response = requests.post(self.host + "/api/Account/RefreshToken", headers=self.get_headers(), json=refresh_data)
        else:
            self.logger.log_trace("Try login with credentials")

            credentials = {
                'username': self.user_name, 
                'password': self.password
            }
            login_response = requests.post(self.host + "/api/Account/Login", headers=self.get_headers(), json=credentials)

        if self.handle_error_status_code(login_response):
            self.logger.log_error("Unable to login with status code " + login_response.status_code + ", Reason: " + login_response.reason)
            return False

        login_response = login_response.json()["data"]
        self.expiration_time = login_response["ExpiresIn"] + self.get_current_time()
        self.auth_token = login_response["AccessToken"]
        self.refresh_token = login_response["RefreshTokenKey"]
        self.expiration_buffer = login_response["ExpiresIn"] * 0.1

        return True

    def get_current_time(self):
        return int(time.time())

    def get_headers(self):
        if self.auth_token is None:
            return {'Content-Type':'application/json'}

        return { 'Content-Type': 'application/json', 'Authorization': 'Bearer ' + self.auth_token }