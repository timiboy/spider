# -*-coding:utf-8-*-

from lxml import etree
import logging
from datetime import datetime
from my_logging import MyLogger
import traceback

logger = MyLogger('parse_html')

# certificate_No: 资格证书号码, practice_No: 执业证编号
def parse_html(content, customer_id):
    tree = etree.HTML(content)

    key = ['name', 'gender', 'certificate_No', 'certificate_status', 'practise_No', 'practise_status',
           'expiration', 'business_domain', 'practise_area', 'company']
    trs = tree.xpath('//ul[@class="xxxx2"]/li/table/tr/td')

    try:
        detail = [i.text for i in trs]

        if len(detail) == len(key):
            return dict(zip(key, detail))
        else:
            logger.warning('error happen when parse html, customer id is %s' % customer_id)
            return None
    except IndexError as e:
        logger.warning(traceback.format_exc())


if __name__ == '__main__':
	from spider import bjh_spider
	content = bjh_spider(name=u'', id_card='')
	print parse_html(content, '123')