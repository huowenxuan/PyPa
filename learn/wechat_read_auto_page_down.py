import wda

wda.DEBUG = False
wda.HTTP_TIMEOUT = 60.0

c = wda.Client('http://localhost:8100')
print(c.status())

# 按下home键
# c.home()

# 保存截图
# c.screenshot('screen.png')

# 输出全屏显示内容，accessible为True为JSON，False为XML
# print(c.source(accessible=True))

# 打开app
s = c.session('com.tencent.weread')

# 屏幕尺寸
print(s.window_size()) # Size(width=414, height=736)

'''
s.tap(200, 600) # 单击
s.double_tap(200, 600) # 双击
s.swipe(x1, y1, x2, y2, 0.5) # 0.5s 扫
s.tap_hold(x, y, 1.0) # 长按 1秒
'''

'''
Find element
# For example, expect: True or False
# using id to find element and check if exists
s(id="URL").exists # return True or False

# using id or other query conditions
s(id='URL')
s(name='URL')
s(text="URL") # text is alias of name
s(nameContains='UR')
s(label='Address')
s(labelContains='Addr')
s(name='URL', index=1) # find the second element. index starts from 0

# combines search conditions
# attributes bellow can combines
# :"className", "name", "label", "visible", "enabled"
s(className='Button', name='URL', visible=True, labelContains="Addr")

# More powerful findding method
s(xpath='//Button[@name="URL"]')
s(classChain='**/Button[`name == "URL"`]')
s(predicate='name LIKE "UR*"')
s('name LIKE "U*L"') # predicate is the first argument, without predicate= is ok
'''

import threading
import random

def toFixed(num, ndigits=2):
    return round(num, ndigits)

def fun_timer():
    # 随机点击坐标
    x = random.randint(300, 400)
    y = random.randint(400, 700)
    s.tap(x, y)
    global timer
    # 随机时间，正常阅读一页的时间为12-30秒
    second = random.uniform(12, 30)
    timer = threading.Timer(second, fun_timer)
    print('点击的坐标为(' + str(toFixed(x)) + ', ' + str(toFixed(y)) + '), ' + str(toFixed(second)) + '秒后再次点击')
    timer.start()

# 打开3秒后开始循环
timer = threading.Timer(3, fun_timer)
timer.start()