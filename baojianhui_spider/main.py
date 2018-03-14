# -*-coding:utf-8-*-

from spider import bjh_spider
from parse_captcha import captcha_recognition
from database import get_mysql_data, RedisHandler, MongoHandler
from parse_html import parse_html
import traceback
import time
from datetime import datetime
from my_logging import MyLogger

rh = RedisHandler()
mh = MongoHandler()

def prepare_work():
    data = get_mysql_data()
    rh.save_to_prepare(data)

logger = MyLogger('main')

def main():
    try:
        while True:
            user = rh.get_from_prepare()
            if not user:
                print 'completed'
                return
            customer_id, name, id_card = user
            print customer_id
            if rh.check_completed(customer_id):
                continue
            html_content = bjh_spider(name, id_card)
            if html_content:
                data = parse_html(html_content, customer_id)
                if data:
                    data['id_card'] = id_card
                    data['customer_id'] = customer_id
                    mh.save_data(data)
            else:
                log = 'error happen, customer_id is %s' % customer_id
                logger.warning(log)
            rh.save_to_completed(customer_id)
            time.sleep(2)
    except:
        logger.warning(traceback.format_exc())