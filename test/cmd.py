import subprocess  # 结果会直接输出到控制台
import time


def touch(x, y):
    subprocess.call('adb shell input tap %s %s' % (x, y), shell=True)


def press_back():
    subprocess.call('adb shell input keyevent 4', shell=True)


def sleep(second):
    time.sleep(second)


while True:
    # 点击第一篇文章的正中央
    touch(175, 800)
    sleep(300)
    press_back()
    sleep(1)
