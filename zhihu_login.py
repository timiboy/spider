# -*- coding: utf-8 -*-

import requests
import json
import re
from hashlib import sha1
import hmac
import time
from requests_toolbelt.multipart.encoder import MultipartEncoder


def get_timestamp():
	return str(long(time.time() * 1000))

def get_signature(timestamp):
	hashed = hmac.new('d1b964811afb40118a12068ff74a12f4', '', sha1)
	hashed.update('password')
	hashed.update('c3cef7c66a1843f8b3a9e6a1e3160e20')
	hashed.update('com.zhihu.web')
	hashed.update(timestamp)
	return hashed.hexdigest()

s = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',}
resp = s.get('https://www.zhihu.com/', headers=headers)

url = 'https://www.zhihu.com/signup?next=//'
resp = s.get(url, headers=headers)
text = resp.text


udid_regex = re.compile(r'&quot;xUDID&quot;:&quot;(.+?)&quot;}')
udid = udid_regex.search(text).group(1)
xsrf_regex = re.compile(r'xsrf&quot;:&quot;(.+?)&quot;')
xsrf = xsrf_regex.search(text).group(1)

url = 'https://www.zhihu.com/api/v3/oauth/captcha?lang=en'
headers = {
    "Accept-Language": "zh-CN,zh;q=0.9", 
    "Accept-Encoding": "gzip, deflate, br", 
    "X-UDID": udid, 
    "Connection": "keep-alive", 
    "accept": "application/json, text/plain, */*", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36", 
    "Host": "www.zhihu.com", 
    "Referer": "https://www.zhihu.com/signup?next=//", 
    "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
}

resp = s.get(url, headers=headers)
print resp.text

headers = {
    "Origin": "https://www.zhihu.com", 
    "Accept-Language": "zh-CN,zh;q=0.9", 
    "Accept-Encoding": "gzip, deflate, br", 
    "X-Xsrftoken": xsrf, 
    "X-UDID": udid, 
    "Connection": "keep-alive", 
    "accept": "application/json, text/plain, */*", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36", 
    "Host": "www.zhihu.com", 
    "Referer": "https://www.zhihu.com/signup?next=//", 
    "authorization": "oauth c3cef7c66a1843f8b3a9e6a1e3160e20"
}

username = 'username'
password = 'password'
timestamp = get_timestamp()
signature = get_signature(timestamp)

payload = {
    "username": "+86%s" % username, 
    "lang": "en", 
    "password": password, 
    "captcha": "", 
    "timestamp": timestamp, 
    "utm_source": "baidu", 
    "source": "com.zhihu.web", 
    "ref_source": "homepage", 
    'grant_type': "password",
    "client_id": "c3cef7c66a1843f8b3a9e6a1e3160e20", 
    "signature": signature,
}

url = 'https://www.zhihu.com/api/v3/oauth/sign_in'
encoder = MultipartEncoder(payload, boundary='----WebKitFormBoundarycGPN1xiTi2hCSKKZ')
headers['Content-Type'] = encoder.content_type

print encoder
resp = s.post(url, headers=headers, data=encoder.to_string())
print resp.status_code
print resp.text

