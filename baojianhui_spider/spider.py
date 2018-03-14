# -*-coding:utf-8-*-
import requests
import time
import os
import traceback
from parse_captcha import captcha_recognition
import random
from my_logging import MyLogger


# 保监会爬虫

def get_timestamp():
	return str(long(time.time() * 1000))

def random_user_agent():
        agents = [
        	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; WOW64; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)',
            'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; ARM; Trident/6.0)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30;'
            ' .NET CLR 3.0.04506.648)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; InfoPath.1',
            'Mozilla/4.0 (compatible; GoogleToolbar 5.0.2124.2070; Windows 6.0; MSIE 8.0.6001.18241)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; EasyBits Go v1.0; InfoPath.1;'
            ' .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
            'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; '
            '.NET CLR 3.0.04506)'
        ]

        return random.choice(agents)


PROXIES = {
	'https':'https://proxyip:1080',
	'http':'http://proxyip:1080',
	
}

logger = MyLogger('bjh_spider')


def bjh_spider(name, id_card):
	try:
		s = requests.Session()
		headers = {'User-Agent':random_user_agent()}
		# url = 'http://iir.circ.gov.cn/web/'
		# s.get(url, headers=headers)

		captcha_url = 'http://iir.circ.gov.cn/web/servlet/ValidateCode?time=%s' % get_timestamp()
		resp = s.get(captcha_url, headers=headers, proxies=PROXIES, timeout=6)
		if not resp.content:
			return None
		print s.cookies.get_dict()
		with open('captcha/%s.jpg' % id_card, 'wb') as f:
			f.write(resp.content)
		captcha = captcha_recognition('captcha/%s.jpg' % id_card)
		os.remove('captcha/%s.jpg' % id_card)
		print captcha

		# url = 'http://iir.circ.gov.cn/web/validateCodeAction!ValidateCode.html?validateCode=%s&dateTime=%s' % (captcha, get_timestamp())
		# resp = s.post(url, headers=headers)
		# captcha_regex = re.compile(r'<state>(\d)</state>')
		# print resp.text
		# if captcha_regex.search(resp.text).group(1) == '6':
		# 	print 'True'

		profile_url = 'http://iir.circ.gov.cn/web/baoxyx!searchInfoBaoxyx.html'
		data = {
			'id_card':id_card[-4:],
			'certificate_code':'',
			'evelop_code':'',
			'name':name.decode('utf-8').encode('gbk'),
			'valCode':captcha
		}
		resp = s.post(profile_url, headers=headers, data=data, proxies=PROXIES, timeout=6)
		return resp.text
	except:
		logger.warning(traceback.format_exc())
		return None

if __name__ == '__main__':
	print bjh_spider(name=u'王五'.encode('utf-8'), id_card='1231231231')