from urllib import request, error, parse
import re
import http
from pybloom_live import BloomFilter

def do_request(url, data={}):
    proxy_used  = ['116.199.2.209:80', '110.73.32.7:6666',
                   '222.76.174.102:8118', '61.155.164.109:3128',
                   '122.72.18.35:80']
    proxy_ok = ['183.166.66.92:808']
    proxy_what = ['58.220.95.107:8080']
    proxy = {'http': proxy_ok[0]}

    proxy_support = request.ProxyHandler(proxy)
    opener = request.build_opener(proxy_support)
    opener.addheaders = [('User-Agent',
                          'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'),
                         ('Accept', 'text/html, */*; q=0.01'),
                         ('Accept-Language', 'zh-CN,zh;q=0.8')
                         ]

    request.install_opener(opener)
    response = request.urlopen(url, parse.urlencode(data).encode('utf-8'))
    return response.read()

    # request_headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36 QQBrowser/4.2.4976.400',
    #     'Accept': 'text/html, */*; q=0.01',
    #     'Accept-Language': 'zh-CN,zh;q=0.8'
    # }
    # req = request.Request(url, headers=request_headers)
    # response = request.urlopen(req)
    # return response.read()

city_home_pages = []
city_ids = []
# dirname = 'mafengwo_notes/'
dirname = 'hainan/'
download_bf = BloomFilter(1024 * 1024 * 16, 0.01)

def download_city_notes(id):
    for i in range(1, 999):
        url = 'http://www.mafengwo.cn/yj/%s/1-0-%d.html' % (id, i)
        if url in download_bf:
            continue

        print('open url' + url)
        htmlcontent = do_request(url).decode('utf-8')

        # 一页中所有的游记，使用正则是因为可以直接拿来url用
        city_notes = re.findall('href="/i/\d{7}.html', htmlcontent)

        if len(city_notes) == 0:
            # 到达最后一页，没有游记
            return
        for city_note in city_notes:
            try:
                city_url = 'http://www.mafengwo.cn%s' % (city_note[6:])
                if city_url in download_bf:
                    continue
                print('download ' + city_url)
                html = do_request(city_url)
                # filename = city_url[7:].replace('/', '_')
                filename = re.search("<title>.*</title>", html.decode('utf-8')).group().strip("</title>")
                # 去掉最后的 ,北京旅游攻略 - 马蜂窝
                pos = filename.rfind(",")
                filename = filename[:pos] + '.html'
                fo = open("%s%s" % (dirname, filename), 'wb+')
                fo.write(html)
                fo.close()
                download_bf.add(city_url)
            except Exception as Arguments:
                print(Arguments)
                continue


try:
    # # 下载目的地首页
    # htmlcontent = do_request('http://www.mafengwo.cn/mdd/').decode('utf-8')
    #
    # # 找出所有城市主页，后五位数字为城市编号
    # city_home_pages = re.findall('/travel-scenic-spot/mafengwo/\d{5}.html', htmlcontent)
    #
    # for city in city_home_pages:
    #     # city_ids.append(city[29:34])
    #     download_city_notes(city[29:34])

    download_city_notes('12938')

except error.HTTPError as Arguments:
    print(Arguments)
except http.client.BadStatusLine:
    print('BadStatusLine')
except Exception as Arguments:
    print(Arguments)
