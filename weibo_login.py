# -*- coding: utf-8 -*-

import requests
import json
import re
import time
import base64
import rsa
import binascii
import random

# 网站主页：https://login.sina.com.cn/signup/signin.php


def get_timestamp():
    return long(time.time()*1000)
def get_su(username):
    return base64.urlsafe_b64encode(username)
def get_sp(pubkey, servertime, nonce):
    pubkey = int(pubkey, 16)
    rsa_pubkey = rsa.PublicKey(pubkey, 65537)
    msg = str(servertime) + '\t' + nonce + '\n' + password
    msg = bytes(msg)
    sp = rsa.encrypt(msg, rsa_pubkey)
    sp = binascii.b2a_hex(sp)
    return sp


s = requests.Session()

username = '123'
password = '123'

prelogin_url ='https://login.sina.com.cn/sso/prelogin.php'
params = {
    "su": get_su(username), 
    "callback": "sinaSSOController.preloginCallBack", 
    "rsakt": "mod", 
    "client": "ssologin.js(v1.4.15)", 
    "entry": "account", 
    "_": get_timestamp()
}

resp = s.get(prelogin_url, params=params)
pre_data = resp.text.lstrip('sinaSSOController.preloginCallBack(').rstrip(')')
pre_data = json.loads(pre_data)

nonce = pre_data['nonce']
pubkey = pre_data['pubkey']
servertime = pre_data['servertime']
data = {
    "useticket": "0", 
    "nonce": nonce, 
    "domain": "sina.com.cn", 
    "savestate": "30", 
    "from": 'null', 
    "service": "account", 
    "encoding": "UTF-8", 
    "sr": "1920*1080", 
    "sp": get_sp(pubkey, servertime, nonce), 
    "servertime": servertime, 
    "su": get_su(username), 
    "rsakv": pre_data['rsakv'], 
    "returntype": "TEXT",
    "vsnf": "1", 
    "pagerefer": "", 
    "entry": "account", 
    "cdult": "3", 
    "gateway": "1", 
    "prelt": "17", 
    "pwencode": "rsa2"
}

headers = {
    "Accept-Language": "zh-CN,zh;q=0.9", 
    "Accept-Encoding": "gzip, deflate, br", 
    "Host": "login.sina.com.cn", 
    "Accept": "*/*", 
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36", 
    "Connection": "keep-alive",
    'Referer': 'https://login.sina.com.cn/signup/signin.php'
}

url  = 'https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.15)&_=%s' % get_timestamp()
resp = s.post(url, headers=headers, data=data)


print json.dumps(json.loads(resp.text), ensure_ascii=False)
print '================================================'
print s.cookies