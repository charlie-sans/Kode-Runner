import logging 
import os
import sys

class logging():
    def __init__(self):
        self.logger = logging.get_logger(self)
        self.logger.setLevel(logging.DEBUG)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.console_handler = logging.StreamHandler(sys.stdout)
        self.console_handler.setLevel(logging.DEBUG)
        self.console_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.console_handler)
        self.file_handler = logging.FileHandler(os.path.join(os.path.dirname(__file__), 'klog.log'))
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.formatter)
        self.logger.addHandler(self.file_handler)
        self.logger.info('Logger initialized')
        
    def get_logger(self):
        return self.logger
    
    def get_formatter(self):
        return self.formatter
    
    def get_console_handler(self):
        return self.console_handler
    
    def get_file_handler(self):
        return self.file_handler
    
    def set_level(self, level):
        self.logger.setLevel(level)
        self.console_handler.setLevel(level)
        self.file_handler.setLevel(level)
        self.logger.info('Logger level set to {}'.format(level))
        
    def set_formatter(self, formatter):
        self.console_handler.setFormatter(formatter)
        self.file_handler.setFormatter(formatter)
        self.logger.info('Logger formatter set')
        
    def set_console_handler(self, console_handler):
        self.logger.addHandler(console_handler)
        self.logger.info('Console handler set')
        
    def set_file_handler(self, file_handler):
        self.logger.addHandler(file_handler)
        self.logger.info('File handler set')
        
    def remove_console_handler(self):
        self.logger.removeHandler(self.console_handler)
        self.logger.info('Console handler removed')
        
    def remove_file_handler(self):
        self.logger.removeHandler(self.file_handler)
        self.logger.info('File handler removed')
        
    def log(self, message):
        self.logger.info(message)
    def debug(self, message):
        self.logger.debug(message)
    def warning(self, message):
        self.logger.warning(message)
    def error(self, message):
        self.logger.error(message)
    def critical(self, message):
        self.logger.critical(message)
        
    def add_console_handler(self):
        self.logger.addHandler(self.console_handler)
        self.logger.info('Console handler added')
        
    def add_file_handler(self):
        self.logger.addHandler(self.file_handler)
        self.logger.info('File handler added')
        
    def remove_all_handlers(self):
        for handler in self.logger.handlers:
            self.logger.removeHandler(handler)
        self.logger.info('All handlers removed')