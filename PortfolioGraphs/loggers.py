import sys, traceback, json, requests, inspect, logging, os
import configuration


def get_executed_file_name():
    frame = inspect.currentframe()
    while frame.f_back:
        frame = frame.f_back

    return frame.f_code.co_filename.split('\\')[-1].split('.')[0]

class Logger(logging.Logger):

    def __init__(self):
        self.log_level = logging.INFO
        self.default_log_format = "%(asctime)s - %(name)s - %(funcName)s - %(lineno)s - %(levelname)s - %(message)s"    

        self.origin_file = get_executed_file_name()

    def get_logger(self, name):
        logging.basicConfig(
            level=self.log_level,
            format=self.default_log_format,
            datefmt='%m/%d/%Y %I:%M:%S %p',
            handlers=[
                logging.StreamHandler(), logging.FileHandler(f"{configuration.LOGS_FOLDER}/logs_{self.origin_file}.log", mode='a')
            ]
        )

        return logging.getLogger(name)
