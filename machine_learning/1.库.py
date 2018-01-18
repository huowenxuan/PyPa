import requests
import os
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy as np
# %matplotlib inline # jupyter命令，设置图表在记事本中可见
import seaborn as sns
import statsmodels.api as sm
# 随机森林分类器
from sklearn.ensemble import RandomForestClassifier
# 将数据分成训练组和测试组的模块
# cross_validation 过时，使用 model_selection
from sklearn.model_selection import train_test_split
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC


# 1. 获取：获取数据
def run1():
    r = requests.get(r'https://api.github.com/users/huowenxuan/starred')
    print(r.json())

# 2. 检查：检查数据
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
    # mean平均值
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


# 2.4 Seaborn 可视化，为统计的可视化而生。可以和Pandas完美协作。基于matplotlib
# 列是特征，行是观测的样例，这种数据框风格称为整洁的数据，是机器学习应用中最常见的形式
# 画出所有的特征
def run7():
    df = get_iris()
    sns.pairplot(df, hue='类别')


# sns和plt结合绘制小提琴图（显示特征的分布情况）
def run8():
    df = get_iris()
    fig, ax = plt.subplots(2, 2, figsize=(7, 7))
    sns.set(style='white', palette='muted')
    # sns 小提琴图
    sns.violinplot(x=df['类别'], y=df['花萼宽度'], ax=ax[0, 0])
    sns.violinplot(x=df['类别'], y=df['花萼长度'], ax=ax[0, 1])
    sns.violinplot(x=df['类别'], y=df['花瓣宽度'], ax=ax[1, 0])
    sns.violinplot(x=df['类别'], y=df['花瓣长度'], ax=ax[1, 1])
    # 总标题
    fig.suptitle('Violin Plots', fontsize=16, y=1.03)
    # 遍历每个子图的轴
    for i in ax.flat:
        # setp设置属性
        plt.setp(i.get_xticklabels(), rotation=-90)
    fig.tight_layout()


# 3 准备：使用Pandas处理（整理）和操作数据
# map，类似数组的map，传入字典或者表达式，操作一列
def run9map():
    df = get_iris()
    # 如果列存在就修改每一行
    df['类别'] = df['类别'].map({'Iris-setosa': 'SET', 'Iris-versicolor': 'VER', 'Iris-virginica': 'VIR'})
    # 如果列不存在就创建这个列并给每行赋值
    df['短类别'] = df['类别'].map({'SET': 'S', 'VER': 'V', 'VIR': 'V'})
    df['备注'] = '这是一条备注'
    # 大于1.3为true，否则为false
    df['宽花瓣'] = df['花瓣宽度'].map(lambda v: '是' if v >= 1.3 else '否') # lambda:使用表达式创建匿名函数


# apply，传入表达式，调用行或列的数据操作一列
def run10apply():
    df = get_iris()
    # 大于1.3为true，否则为false
    df['宽花瓣'] = df['花瓣宽度'].apply(lambda v: '是' if v >= 1.3 else '否')
    # 在整个数据框上使用apply，调用行的数据来修改列; axis=1为对行进行操作，axis=0为对列进行操作
    df['花瓣面积'] = df.apply(lambda r: r['花瓣宽度'] * r['花瓣长度'], axis=1)


# applymap，操作所有数据单元
def run11applymap():
    df = get_iris()
    # 对所有的数据单元都执行一遍函数。在所有的float类型后面加√
    df = df.applymap(lambda v: str(v) + '√' if isinstance(v, float) else v)


# groupby
def run12groupby():
    df = get_iris()
    # 为类别分类，并求出均值
    df.groupby('类别').mean()
    # 获取每个类别完全的描述性统计信息
    df.groupby('类别').describe()
    # 通过和每一个唯一类相关联的花瓣宽度???，对类别进行分组
    df.groupby('花瓣宽度')['类别'].unique().to_frame()
    # 将每个类别的最大最小值、间距组成一个数据框。agg返回一个将字典键值作为列名的数据框
    df.groupby('类别')['花瓣宽度'].agg({'间距': lambda x: x.max() - x.min(), '最大': np.max, '最小': np.min})


# 4. 建模和评估
# 4.1 建模 statsmodels: 探索数据、评估模型，运行统计检查
# 构建线性回归模型，为花萼宽度和花萼长度之间的关系建模
def run13sm_ols():
    df = get_iris()
    # 1. 先通过散点图来目测两者的关系
    fig, ax = plt.subplots(figsize=(7, 7))
    ax.scatter(df['花萼宽度'][:50], df['花萼长度'][:50])
    ax.set_ylabel('Length')
    ax.set_xlabel('Width')
    ax.set_title('Setosa width vs. length', fontsize=14, y=1.02)
    # 2. 似乎有一个正向的线性关系，使用sm在这个数据集上运行一个线性回归模型，预估这种关系的强度
    y = df['花萼长度'][:50]
    x = df['花萼宽度'][:50]
    x2 = sm.add_constant(x)
    # OLS 线性回归 普通最小二乘法
    results = sm.OLS(y, x2).fit()
    # 输出模型
    print(results.summary())
    # 3. 绘制回归线
    fig, ax = plt.subplots(figsize=(7, 7))
    # fittedvalues 获取从模型所得的回归线
    ax.plot(x, results.fittedvalues, label='regression line')
    ax.scatter(x, y, label='data point', color='b')
    ax.set_ylabel('花萼长度')
    ax.set_xlabel('花萼宽度')
    ax.set_title('Setosa width vs. length', fontsize=14, y=1.02)
    ax.legend(loc=2)


# 4.2 评估 scikit-learn(sklearn)：文档好，接口统一。分类、回归、聚类、降维、模型选择、预处理
def run14sklearn_random():
    df = get_iris()
    # 实例化随机森林分类器，
    clf = RandomForestClassifier(max_depth=5, n_estimators=10)
    x = df.ix[:, :4]
    y = df.ix[:, 4]
    # 创建了X矩阵和y向量。iris数据的四个特征：花瓣花萼的宽度和高度，成为独立特征矩阵X。
    # train_test_split 打乱数据的先后顺序，因为原有的顺序可能包含误导实际预测的信息，把数据打乱分成四个子集
    # test_size 0.3意味着将数据的30%分配给测试X_test和y_test，其余的被分配到训练的部分X_train和y_train
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=.3)
    # 训练 fit。使用训练数据来拟合模型
    clf.fit(X_train, y_train)
    # 预测。一旦模型训练完毕，再通过测试数据来调用分类器的预测方法。
    # 注意：测试数据是分类器没有处理过的数据，预测的返回结果是预估标签的列表。
    y_pred = clf.predict(X_test)

    # 创建对应实际标签和预估标签的数据框
    rf = pd.DataFrame(list(zip(y_pred, y_test)), columns=['predicted', 'actual'])
    rf['correct'] = rf.apply(lambda r: 1 if r['predicted'] == r['actual'] else 0, axis=1)
    print(rf)
    # 准确率：加和正确的预测次数，并将其除以样例总数，获取准确率
    print(rf['correct'].sum()/rf['correct'].count())

    # 看哪些特征提供了最佳的预测能力
    # feature_importances_ 返回特征在决策树中划分叶子节点的相对能力，总和为1，越大的特征约好
    # 最终得到花瓣的长度和宽度对于区分iris的类别有很好的辨别力
    f_importances = clf.feature_importances_
    f_names = df.columns[:4]
    f_std = np.std([tree.feature_importances_ for tree in clf.estimators_], axis=0)

    zz = zip(f_importances, f_names, f_std)
    zzs = sorted(zz, key=lambda x: x[0], reverse=True)
    imps = [x[0] for x in zzs]
    labels = [x[1] for x in zzs]
    errs = [x[2] for x in zzs]
    plt.bar(range(len(f_importances)), imps, color='r', yerr=errs, align='center')
    plt.xticks(range(len(f_importances)), labels)


# 切换分类器，并使用支持向量机SVM，而不是随机森林
def run15sklearn_svm():
    df = get_iris()
    clf = OneVsRestClassifier(SVC(kernel='linear'))
    X = df.ix[:, :4]
    y = np.array(df.ix[:, 4]).astype(str)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.3)
    clf.fit(X_train, y_train)

    t_pred = clf.predict(X_test)

    rf = pd.DataFrame(list(zip(t_pred, y_test)), columns=['predicted', 'actual'])
    rf['correct'] = rf.apply(lambda r: 1 if r['predicted'] ==
                                            r['actual'] else 0, axis=1)
    print(rf)
    print(rf['correct'].sum()/rf['correct'].count())



def get_iris():
    return pd.read_csv('/Users/huowenxuan/Desktop/py/machine_learning/outputs/iris/iris.data',
                       names=['花萼长度', '花萼宽度', '花瓣长度', '花瓣宽度', '类别'])


run15sklearn_svm()
