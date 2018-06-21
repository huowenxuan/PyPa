'''
以太阳为原点构建三维坐标系
月球轨道平面（白道面）与地球公转轨道平面（黄道面）的夹角为5.145396
黄道面在x-y平面上
'''

import numpy as np
import matplotlib as mpl

mpl.use('TKAgg')

from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animmation

# 日地距离r1为1.5亿千米，月地距离r2为38.4万千米，日地为月地的390.625倍
# 为了方便显示，可分别设置为10和1
sun_earth_dist = 10
sun_moon_dist = 1
# 地球对太阳做匀速圆周运动的角速度。2π
sun_earth_angular_speed = 2 * np.pi
# 月球相对地球做匀速圆周运动的角速度。24π
earth_moon_angular_speed = 24 * np.pi

sun_size = 20
earth_size = 8
moon_size = 4
sun_color = 'red'
earth_color = 'blue'
moon_color = 'grey'

# 太阳坐标
sun_x = 0
sun_y = 0
sun_z = 0

# 时刻的数组，表示星体公转一周，从0到1，以0.005递增
t_range = np.arange(0, 1 + 0.005, 0.005)
# 从0到0.995，以0.005递增
t_drange = np.arange(0, 1, 0.005)
t_len = len(t_range)
t_dlen = len(t_drange)

# 地球在某一时刻的坐标（的集合）
'''

'''
earth_x = sun_x + sun_earth_dist * np.cos(sun_earth_angular_speed * t_range)
earth_y = sun_y + sun_earth_dist * np.sin(sun_earth_angular_speed * t_range)
earth_z = sun_z + np.zeros(t_len)

phi = 5.145396 * np.pi / 180

# 月球在某一时刻的坐标（的集合）（联立向量夹角公式）
moon_x = earth_x + sun_moon_dist * np.sin(earth_moon_angular_speed * t_range)
moon_y = earth_y + sun_moon_dist * np.cos(earth_moon_angular_speed * t_range) / (np.cos(phi) * (1 + np.tan(phi)))
moon_z = earth_z + (moon_y - earth_y) * np.tan(phi)


# 计算
# 计算某个时刻所有星球的位置
def cal_for_t(t):
    xt1 = sun_x + sun_earth_dist * np.cos(sun_earth_angular_speed * t)
    yt1 = sun_y + sun_earth_dist * np.sin(sun_earth_angular_speed * t)
    zt1 = sun_z
    xt2 = xt1 + sun_moon_dist * np.sin(earth_moon_angular_speed * t)
    yt2 = yt1 + sun_moon_dist * np.cos(earth_moon_angular_speed * t) / (np.cos(phi) * (1 + np.tan(phi) ** 2))
    zt2 = zt1 + (yt2 - yt1) * np.tan(phi)
    xt21 = xt1 + sun_moon_dist * np.sin(2 * np.pi * t_range)
    yt21 = yt1 + sun_moon_dist * np.cos(2 * np.pi * t_range) / (np.cos(phi) * (1 + np.tan(phi) ** 2))
    zt21 = zt1 + (yt21 - yt1) * np.tan(phi)

    return (xt1, yt1, zt1, xt2, yt2, zt2, xt21, yt21, zt21)


def init():
    global line1, line2, line3
    ti = 0
    t = t_drange[np.mod(ti, t_dlen)]

    data = cal_for_t(t)

    line1, = ax.plot([data[0]], [data[1]], [data[2]], marker='o', color=earth_color, markersize=earth_size)
    line2, = ax.plot([data[3]], [data[4]], [data[5]], marker='o', color=moon_color, markersize=moon_size)
    line3, = ax.plot(data[6], data[7], data[8], color='purple')
    return line1, line2, line3


def update_lines(data):
    global line1, line2, line3
    line1.set_data(data[0], data[1])
    line1.set_3d_properties(data[2])
    line2.set_data(data[3], data[4])
    line2.set_3d_properties(data[5])
    line3.set_data(data[6], data[7])
    line3.set_3d_properties(data[8])
    return line1, line2, line3


def data_gen():
    arr = []
    for ti in range(1, t_dlen):
        t = t_drange[ti]
        data = cal_for_t(t)
        arr.append([data[0], data[1], data[2], data[3], data[4], data[5], data[6], data[7], data[8]])
    return arr


# 生成图表的大小
f = plt.figure(figsize=(6, 6))
ax = f.add_subplot(111, projection='3d')
# 高宽比，'equal' / 数字
ax.set_aspect('equal')
ax.set_title("Sun-Earth-Moon Model")

ax.plot([0], [0], [0], marker='o', color=sun_color, markersize=sun_size)
ax.plot(earth_x, earth_y, earth_z, 'r')
ax.plot(moon_x, moon_y, moon_z, 'b')
ax.set_xlim([-(sun_earth_dist + 2), (sun_earth_dist + 2)])
ax.set_ylim([-(sun_earth_dist + 2), (sun_earth_dist + 2)])
ax.set_zlim([-5, 5])

# init()

ani = animmation.FuncAnimation(f, update_lines, frames=data_gen(), init_func=init, interval=20)
plt.show()
