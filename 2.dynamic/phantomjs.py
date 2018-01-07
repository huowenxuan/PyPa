from selenium import webdriver

# --ignore-ssl-errors=true|false 忽略浏览器证书错误（例如12306永远没有CA授权）
# --load-images=true|false 是否加载图片，如果不加载图片，加快加载速度，节省流量，滚动范围会更小，更容易翻页爬取
# --disk-cache=true|false
driver = webdriver.PhantomJS(service_args=['--ignore-ssl-errors=true'])
# 动态网页，可能存在大量数据是根据视图来动态加载的，可以模拟窗口大小
# 如果设置的过小，不得不使用js的scroll来模拟滚动，所以设置一个相对较大的高度来显示
driver.set_window_size(1280, 2400)
driver.get(url)
content = driver.page_source
# 如果不退出，PhantomJS会一直在后台并占用系统资源
# 但是不能保证一定会关掉
driver.close()
driver.quit()

# 第二种配置方法，设置一个外部的配置文件
driver2 = webdriver.PhantomJS(service_args=['--config=/path/to/config.json'])

# config.json:
{
    /* Same as: --ignore-ssl-errors=true */
    "ignoreSslErrors": true,
    "maxDiskCacheSize": 1000,
    "outputEncoding": "utf8"
}