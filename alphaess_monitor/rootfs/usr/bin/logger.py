LogLevels = {
    "Fatal": 0,
    "Error": 1,
    "Warning": 2,
    "Notice": 3,
    "Info": 4,
    "Debug": 5,
    "Trace": 6
}


class Logger:
    def __init__(self, log_level):
        self.log_level = log_level

    def log(self, level, message):
        if int(self.log_level) >= int(level):
            print(message)

    def log_info(self, message):
        self.log(LogLevels["Info"], message)

    def log_debug(self, message):
        self.log(LogLevels["Debug"], message)

    def log_error(self, message):
        self.log(LogLevels["Error"], message)

    def log_warn(self, message):
        self.log(LogLevels["Warning"], message)

    def log_notice(self, message):
        self.log(LogLevels["Notice"], message)

    def log_fatal(self, message):
        self.log(LogLevels["Fatal"], message)

    def log_trace(self, message):
        self.log(LogLevels["Trace"], message)
