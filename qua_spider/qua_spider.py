# -*- coding:utf-8 -*-
# 通过手机页面进行抓取

import json
import requests
import warnings
import pandas as pd
from redis import Redis
from pymongo import MongoClient
from datetime import datetime
from urllib3.connectionpool import InsecureRequestWarning

warnings.filterwarnings(action='ignore', category=InsecureRequestWarning)


class RedisHandler():
    def __init__(self, url='redis://localhost:6379/0'):
        self.rh = Redis.from_url(url=url)

    def insert(self, city):
        self.rh.sadd('CITY_LIST', city)

    def exists(self, city):
        if self.rh.sismember('CITY_LIST', city):
            return True
        return False

    def clear(self):
        self.rh.delete('CITY_LIST')


class MongoHandler():
    def __init__(self, host='127.0.0.1', port=27017):
        self.mh = MongoClient(host=host, port=port)

    def insert(self, hotel_info):
        self.mh.db.hotel_info.insert(hotel_info)

    def gen_excel(self):
        data = self.mh.db.hotel_info.find()
        result = []
        for each in data:
            result.append({
                'city': each['city'],
                'name': each['name'],
                'address': each['address'],
                'price': each['price']
            })
        df = pd.DataFrame(result)
        df.to_excel('result.xlsx', encoding='gb18030', index=False)


RH = RedisHandler()
MH = MongoHandler()


def get_city():
    '''
    :return: {'name':'city_name', 'cityurl':'city_url'} 
    '''
    citylist_url = 'http://hotel.qunar.com/render/hoteldiv.jsp?&__jscallback=XQScript_8'
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36',
    }

    resp = requests.get(citylist_url, headers=headers)
    citylist = json.loads(resp.text.lstrip('XQScript_8(').rstrip(')'))
    for intercity in citylist.get('hotCityConfig', {}).get('data', {}).get('intercity', {}).values():
        for city in intercity.get('cityList', [])[0].get('list', []):
            yield city


def spider(checkInDate='2018-11-30', checkOutDate='2018-12-01'):
    for city in get_city():
        city_name = city.get('name', '')
        city_url = city.get('cityurl', '')
        if city_name and city_url:
            if RH.exists(city_name):
                continue
            RH.insert(city_name)
            print u'正在抓取 %s 的酒店信息...' % city_name
            hotellist_url = 'https://touch.qunar.com/api/v8/hotel/hotellist'
            params = {
                'city': city_name,
                'cityUrl': city_url,
                'checkInDate': checkInDate,
                'checkOutDate': checkOutDate,
                'page': 0
            }
            headers = {
                'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Mobile Safari/537.36',
                'Host': 'touch.qunar.com',
                'Connection': 'keep-alive',
                'Accept': 'application/json, text/plain, */*',
            }
            while params['page'] < 50:
                params['page'] += 1
                print 'page %d' % params['page']
                resp = requests.get(hotellist_url, params=params, headers=headers, verify=False)
                hotellist = json.loads(resp.text)
                hotels = hotellist.get('data', {}).get('hotels', [])
                if hotels:
                    for hotel in hotels:
                        data = {
                            'city': city_name,
                            'name': hotel.get('attrs', {}).get('hotelName', ''),
                            'address': hotel.get('showAddr', ''),
                            'price': hotel.get('price', ''),
                            'image': hotel.get('attrs', {}).get('imageID', ''),
                            'detail_info': json.dumps(hotel),
                            'create_time': datetime.now()
                        }
                        MH.insert(data)
                else:
                    break

if __name__ == '__main__':
    spider()
    MH.gen_excel()