# -*-coding:utf-8-*-

import logging
from datetime import datetime

class MyLogger():
    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.handler = logging.FileHandler(filename='logging/%s.log' % name)
        self.logger.addHandler(self.handler)

    def warning(self, info):
        msg = '%s : %s \n==========================\n' % (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), info)
        self.logger.warning(msg)


if __name__ == '__main__':
    logger = MyLogger('test')
    logger.warning('test msg')