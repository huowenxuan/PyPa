'''
针对钓鱼网站
'''

import requests, random
from urllib import request, parse

def hehe(n, p):
    url = 'http://rtqt.nbwsg.cn/mail/save.asp'
    proxy_ok = ['116.199.2.209:80']
    proxy_what = ['222.76.174.102:8118']

    proxy = {'http': proxy_ok[0]}
    try:
        proxy_support = request.ProxyHandler(proxy)
        opener = request.build_opener(proxy_support)
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]

        request.install_opener(opener)
        data = {'u': n, 'p': p, 'verifycode': 922}
        response = request.urlopen(url, parse.urlencode(data).encode('utf-8'))
        print(response.read().decode('gbk'))
    except Exception as err:
        print("出错了")

count = 0
while count >= 0:
# for i in range(1, 10000):
    count += 1
    n = str(random.randint(123456789, 9999999999))
    p = "".join(random.sample('1234567890qwertyuiop[];lkjhhgfdsazxcvbnm@#', 10))
    print(str(count) + '次' + '  ' + n + '   ' + p)
    hehe(n, p)
