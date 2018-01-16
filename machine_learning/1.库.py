import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy as np
# %matplotlib inline # jupyter命令，设置图表在记事本中可见
import seaborn as sns

# 1. 获取
def run1():
    r = requests.get(r'https://api.github.com/users/huowenxuan/starred')
    print(r.json())

# 2. 检查
# 2.1 IPython jupyter 基于Web的交互性Python运行环境，类似命令行实时输出显示结果
# pip3 install ipython
# pip3 install jupyter
# jupyter notebook 从网页打开jupyter，右边new弹出下拉，选择Python3即可进入命令行运行，shift+enter运行

def get_iris():
    # PATH = r'./outputs/iris/'
    PATH = '/Users/huowenxuan/Desktop/py/machine_learning/outputs/iris/'
    filename = 'iris.data'
    # r = requests.get('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data') # 已经保存在了./source_data/iris.data中，是一个CSV文件
    # with open(PATH + filename, 'w') as f:
    #     f.write(r.text)
    # pd解析文件，names设定列名，如果源文件有标题行，pandas会自动解析这一行
    # pd操作的基本单位是表格形式的数据列和行，数据列成为系列Series，表格成为数据框DataFrame
    return pd.read_csv(PATH + filename, names=['花萼长度', '花萼宽度', '花瓣长度', '花瓣宽度', '类别'])

# 2.2 Pandas 数据分析工具
def run2():
    df = get_iris()
    # 转换为表格
    df.head()
    # 通过列名获取这一行
    df['花萼长度']
    # .ix[row, column]前几行和前几列
    df.ix[:3, :2]
    # 条件查询，获取具备条件的列
    df.ix[:3, [x for x in df.columns if '宽度' in x]]
    # unique将获取到的值保存在set中，并返回set。也就是相同的值只选择其中一个
    df['类别'].unique()
    # 获取只包含Iris-virginica类的数据
    data = df[df['类别'] == 'Iris-virginica']
    # 获取结果的数量
    data.count()
    # 上面的数据保留了原始的索引，将这些数据保存到一个新的数据并重置索引
    data = data.reset_index(drop=True)
    # 添加条件
    data = df[(df['类别'] == 'Iris-virginica') & (df['花瓣宽度'] < 2.2)]
    # 描述性统计数据
    data = df.describe()
    # 传入自定义的百分比，获取更详细的信息
    data = df.describe(percentiles=[.20, .40, .80, .90, .95])
    # 查看特征之间的相关性。参数method="spearman" / "kendall"？ 不懂
    data = df.corr()

# 2.3 Matplotlib 可视化 仿效MATLAB的绘图功能

# 显示花瓣宽度直方图
def run3():
    df = get_iris()
    # 创建宽6英寸，高4英寸的插图（条形图）
    fig, ax = plt.subplots(figsize=(6,4))
    # 导入数据并且设置柱子颜色
    ax.hist(df['花瓣宽度'], color='black')
    # 放置标签
    ax.set_ylabel('Count', fontsize=12)
    ax.set_xlabel('Width', fontsize=12)
    # 为全图设置标题，y:相对于图片顶部的位置
    plt.title('Width', fontsize=14, y=1.01) # 插图中无法显示中文

# 为每一列生成直方图
def run4():
    df = get_iris()
    # 2x2
    fig, ax = plt.subplots(2, 2, figsize=(6, 4))
    # 左上
    ax[0][0].hist(df['花瓣宽度'], color='black')
    ax[0][0].set_ylabel('Count', fontsize=12)
    ax[0][0].set_xlabel('Width', fontsize=12)
    ax[0][0].set_title('Iris Sepal Width', fontsize=14, y=1.01)

    ax[0][1].hist(df['花萼宽度'], color='black')
    ax[0][1].set_ylabel('Count', fontsize=12)
    ax[0][1].set_xlabel('Width', fontsize=12)
    ax[0][1].set_title('Iris Petal Width', fontsize=14, y=1.01)

    ax[1][0].hist(df['花瓣长度'], color='black')
    ax[1][0].set_ylabel('Count', fontsize=12)
    ax[1][0].set_xlabel('Width', fontsize=12)
    ax[1][0].set_title('Iris Petal Length', fontsize=14, y=1.01)

    ax[1][1].hist(df['花萼长度'], color='black')
    ax[1][1].set_ylabel('Count', fontsize=12)
    ax[1][1].set_xlabel('Width', fontsize=12)
    ax[1][1].set_title('Iris Sepal Length', fontsize=14, y=1.01)

    # 调整图表位置，避免拥挤
    plt.tight_layout()

# 散点图
def run5():
    df = get_iris()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(df['花瓣宽度'], df['花瓣长度'], color='green')
    ax.set_ylabel('花瓣宽度')
    ax.set_xlabel('花瓣长度')
    ax.set_title('Scatterplot')

# 折线图
def run6():
    df = get_iris()
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(df['花瓣宽度'], color='blue')
    ax.set_ylabel('index')
    ax.set_xlabel('Width')
    ax.set_title('Width Plot')

# 条形图 堆积条形图
def run6():
    df = get_iris()
    fig, ax = plt.subplots(figsize=(6, 6))
    bar_width = .8
    labels = [x for x in df.columns if '宽度' in x or '长度' in x]
    ver_y = [df[df['类别'] == 'Iris-versicolor'][x].mean() for x in labels]
    vir_y = [df[df['类别'] == 'Iris-virginica'][x].mean() for x in labels]
    set_y = [df[df['类别'] == 'Iris-setosa'][x].mean() for x in labels]
    # x坐标显示的长度
    x = np.arange(len(labels))
    # 绘制每个条形，bottom参数将该序列的y点最小值设置为下面那个序列的y点最大值
    ax.bar(x, vir_y, bar_width, bottom=set_y, color='darkgrey')
    ax.bar(x, set_y, bar_width, bottom=ver_y, color='white')
    ax.bar(x, ver_y, bar_width, color='black')
    # 条形之间的间隔
    ax.set_xticks(x+(bar_width/2))
    # 列名
    ax.set_xticklabels(labels, rotation=-70, fontsize=12)
    ax.set_title('每个类别中特征的平均衡量值', y=1.01)
    # 添加图例描述每个序列
    ax.legend(['virginica', 'setosa', 'versicolor'])

# 2.4 Seaborn 可视化 专门为统计可视化而创建的库。可以和Pandas完美协作。列是特征，行是观测的样例，这种数据框风格称为整洁的数据，是机器学习应用中最常见的形式

# 画出所有的特征
def run7():
    df = get_iris()
    sns.pairplot(df, hue='类别')

# 3 准备
# 4 建模和评估

def get_iris():
    return pd.read_csv(
        '/Users/huowenxuan/Desktop/py/machine_learning/outputs/iris/iris.data',
        names=['花萼长度', '花萼宽度', '花瓣长度', '花瓣宽度', '类别']
    )

run7()