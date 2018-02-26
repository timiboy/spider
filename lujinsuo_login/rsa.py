# -*- coding:utf-8 -*-

import execjs

with open('rsa.js', 'r') as f:
	rsa_js = f.read()
js = execjs.compile(rsa_js)

def rsa_encrypt(pwd):
	return js.call('run', pwd)