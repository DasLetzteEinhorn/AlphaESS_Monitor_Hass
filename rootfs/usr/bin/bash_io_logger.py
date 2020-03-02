import os


class BashIoLogger:
    def __init__(self):
        pass

    def log(self, level, message):
        # TODO: Not working in /bin/sh context. Move to bashio context or find other solution.
        os.system("bashio::log." + level + " '" + message.replace("'", "\\'") + "'")

    def log_info(self, message):
        self.log("info", message)

    def log_debug(self, message):
        self.log("debug", message)

    def log_error(self, message):
        self.log("error", message)

    def log_warn(self, message):
        self.log("warn", message)

    def log_notice(self, message):
        self.log("notice", message)

    def log_fatal(self, message):
        self.log("fatal", message)

    def log_trace(self, message):
        self.log("trace", message)
