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

# 准备函数， 最初运行主函数前应该运行这个函数
def prepare_work():
    data = get_mysql_data()
    rh.save_to_prepare(data)

logger = MyLogger('main')

# 主函数
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
                rh.save_to_completed(customer_id)   # 现在只有顺利抓取了内容才存入已爬表
            else:
                log = 'error happen, customer_id is %s' % customer_id
                logger.warning(log)
            time.sleep(2)
    except:
        logger.warning(traceback.format_exc())


# 补偿函数，请确保在没有main函数运行的情况下才执行
def repair(filename='logging/main.log'):
    rh.check_log(filename)