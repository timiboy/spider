# -*- coding:utf-8 -*-

import requests
import time
from rsa import rsa_encrypt

# 主页 https://user.lu.com/user/login

def get_timestamp():
    return str(long(time.time() * 1000))

username = 'username'
password = 'password'

session = requests.Session()


headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.140 Safari/537.36'
}

accept_device_url = 'https://info.lu.com/sec-info/service/mq/accept-device-info'
data = {
    'deviceKey':'78BDC44E9C19957FAF163A5339B074E0C9A1C2D4AE43612CC2D5AF94C477465FC7666A9B8F7C76DCE06489FD2049D485186ECDF4BF60A60F79F37C580CC5EDF4032D1CF00DF92BFC5CD11E3B0C9EED77C40F35560BCDBAE8518C5A40948FD7B41760CA8B6D67306ECB031C08EBEC7B54E661600D525D2F7BD1AF49C58FED0AE8',
    'deviceInfo':'SOtXUciknx4d4I69gahYBPkwMZsePGJUDEYot2hsAz3FdN523HEY9ytwcEajKMridFB/6Lyo4qSPA1MZ+zkWSHTPGauB4K0VqI27pnsaE+y19c/q8icAxLRExkKHds+PBr5Elklq0utjn/Dr1f5ga2QLvbIMW1d8AQ6mF+ANBD9h0Ovi+Iq2r4ZdZJFmAw3avNdcHHJ0buT3y4tQHqaheGiV11us7zwWt79ASZ5DYdebpExRWEdigASV7OYimOYUgn+JmMNrYsYjhQX/rj88u7ntHYyhCBIO9xVJmSxurNipet9dgIZTqzrOIXQFbCnIJ/FK2F92gYD1mwiOjSnWQ6M+9V0JDkIO22KVWlZQBw8e3XO/ypNmrJA+5NngOjKhXKoLnBtSq9ezYh2nOMnW2nWt34LFMjMhbrnaTIoS8BoM+s3CO4fgZVXLR+mtx16LmILhOrj6qIsZf1yiJ20Cm40IsKmXuz+m+bVAhkk2W6Byza40yOKaa6zUV1YpOfwv9VS919MP6YP0MHuQfAOTiZqGtxtdhIGkoESh79XtpWNz7BfD6+lmxzwac+pCheneL8WntQothdNrVESlA5wAUBuiFW79JrFj2c1FiE844gumns5g+qOoXSrgFuhZj+C4KB/IuiCNENIBQEKNgEoKynmzHV0uOHuM4dQs1WbaRtoKBfCzAQwpFzkLMOdKGyJCLD3/aJAgroC2A5/RpaMzitzvqzo5pqssOZ9cC00C0EjcNUeErSJfc6UbKfi3sopPPpQHLqAQZRPsloOxhnjLI8Ppu3WViiZiDZlbqBD4aG0dFbU9kv2It/y61sOLzxCbCg9bBlbptrixTDyAkqrZobBE6yqT0yW8x3IUAVgFSQUdFbU9kv2It/y61sOLzxCbj+qAHDHcDbsTnDdsumHp0mO/d+WGosuqeSWGUdrzqin6tqgj6dWuT90Fnafa8mDFoWtqkLY/p4J7xtWYObmkdfHBRRYS7ka1SLSgTok6yKLiUvVOlQUyYGI3/DPe/MuQBSucAsGp+A9GRjheRdQtf3ztlW2BLRRzj+RstMb/LNjn4xbBEDAq4i9+8lrMzBq+Ro+oWFLkkBLIt21Dkycfa1jP03Oqrj3FngdsxDcToFgYquF5+MOfDwE3+18RZWJbWABBl0jjNq7GNRcsLHlx36KQvLWbbhFMyIsIzNu8hnkr9TQ16flCMJ9yZUfWKpLAPX8SRuDzmRye9R7EKu3vX8be6y07tzrUWxDnlNvdtPQduEN/kngZnrjIgD2mGttMSZK4/l79eQ6XaMin+FmcWVrFkrQpoCtRw94/qqZl+7AiDwUtJJgJdLLkL6cLZhoolUgyH5JSIVoiWy62boj0Z03j2Po8s254FnIkH/TZP8mmFuODW58GbkrYdl89UZfJFJgDPGVBA7bCh92fdP7yBtzwknNnAuZmmZlCjEIjm5Er9TQ16flCMJ9yZUfWKpLAMLdLrdGQWJYzDZL8y0kJSjLW2ul1HwSsJayFaUch1YaHV5X21S3it060TNx9hTcKKx3GYbWs7v9OWsF718+ZiOfqMQvE1IyzWEnF7A/b/yL17ZGGfiTryiaPXrfqxtNFRGeg0U7/gCHqS4z3L6zYsVoNtePL2ZcLHj+PvjmLry8CiS9MniCMcxJD/dafOgqKgGqvQXbnEmTJESZbphAMnfY1+KV0lRY/ouw19GcIQZbvYW5AtguFgFxNocTK6T3Se50SXHbQtXApDyqNPxnSsxEnrrT5DmdFV+XUvJ8KTZNHZUvFBd0JH/yq3wZdlBXa9dKHOV7NZ0cVcypkQ0O6Mx24Q3+SeBmeuMiAPaYa20xxvzK+TC1kqQr1WrqH0IBnN4yWyPAblEocO0XlD4bHxA11Qnr0puW4Jm3RpoLWG20TJdFU7o+OFGNJO8ArVwIERYhxl7GCFYHQfxO2hTnn+PXShzlezWdHFXMqZENDujMaIb4tzURRK18vsWeXEweWdUs3G/c/8/eLSh9HagKT+dEI19GnVGBYO8PqInjz8XrKleAB047yQWJF8uY/kEWVQz2+JyyTJIUutwJnU91c/c/UhRgD+ONlQjJgsgHo7/TPPGcP3fQJEgM4CjCIiW2bT7nolGMuMJ9bHpbg/unNTTGmRbat80a6BpZdWDU2KfW8zNuYyzfpVIOWmx8T825WuAn9kP7ds3FFkCaZoOuh/wH2mLdN3zxkYzIMzPq3VIoeSQ2ERxWxTUwk14sv1VBmpQkab6I6F07K3Ibq4jxZ1OvYsKQL9Q75956xQgYGjZ43UbZWooqUlHEbzFqJigwS2dKNtNGrLZ3f4XJQPgESQm19m9kWGFB0Q1W93WCKff7oVUWPDb3GR4007N79cE7ljLocRtuiarHYxSgRrJQfgpnvgi3JbU+MZ+z/wO5lVl4='
}

resp = session.post(accept_device_url, headers=headers, data=data)
print resp.text

# ======================= 获取验证码 ====================================
get_captcha_url = 'https://user.lu.com/user/captcha/captcha.jpg'
params = {
    'source':'login',
    '_':get_timestamp()
}
resp = session.get(get_captcha_url, params=params, headers=headers)
with open('captcha.jpg', 'wb') as f:
    f.write(resp.content)

captcha = raw_input(u'请输入验证码:')

# ========================== 检查验证码输入是否正确 ===================================
check_captcha_url = 'https://user.lu.com/user/captcha/pre-check'
params = {
    'inputValue':captcha,
    'source':'login',
    '_':get_timestamp()
}
resp = session.get(check_captcha_url, headers=headers, params=params)
result = json.loads(resp.text)
print result
if result.get('result') == 'SUCCESS':
	# ========================== 验证码输入正确则进行登录 ====================================
	login_url = 'https://user.lu.com/user/login'
	data = {
	    'isTrust':'Y',
	    'password':rsa_encrypt(password),
	    'openlbo':'0',
	    'deviceKey':'1DA04D5FA06A3DF9351172402D3736E93F5AD7BB4422E6181D17A9C9FE55ABD323517C5B01B09D1254E255600623E57D294B58C7CDAEF4FAA973316CFCAA9CE4E8DD889CF3874E1E9AFFF57FAED8789446D8C69DED5D2EDBAFC73A3B262BF9ED060D16D364AC30720DF3B707A1E81DC89D36822E679D61A3B732A28A02D84678',
	    'deviceInfo':'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',
	    'loginFlag':'2',
	    'hIsOpenLboAccStatus':'0',
	    'hIsSignLboUserCrsChecked':'0',
	    'userName':username,
	    'pwd':'************',
	    'validNum':captcha,
	    'agreeLbo':'on',
	    'agreeLbo':'on',
	    'agreeLbo':'on',
	    'agreeLbo':'on',
	    'loginagree':'on'
	}

	resp = session.post(login_url, headers=headers, data=data)
	print resp.text