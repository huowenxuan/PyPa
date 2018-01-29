import re
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import statsmodels.api as sm
import patsy

plt.style.use('ggplot')
import folium

pd.set_option("display.max_columns", 30)
pd.set_option("display.max_colwidth", 100)
pd.set_option("display.precision", 3)

'''
1. =========获取数据=========
'''
# CSV_PATH = r'C:/Users/msi/Desktop/py/machine_learning/source_data/magic.csv'
CSV_PATH = r'/Users/huowenxuan/Desktop/py/machine_learning/source_data/magic.csv'
'''
2. =========准备数据（格式化）=========
'''
df = pd.read_csv(CSV_PATH)
# 所有的列标题
df.columns
# 查看数据
df.head()
# 转置数据，并垂直显示，不能使用print，格式不对，要在jupyter中显示
df.head().T

# 发现有些数据有缺失值，需要多个操作来标准化数据，发现有两种类型的房源，单个单元和多个单元，需要进行区分
# 根据listingtype_valued字段，把数据拆分为单一的单元和多个单元
# mutlpitle units
mu = df[df['listingtype_value'].str.contains('Apartments For')]
# single units
su = df[df['listingtype_value'].str.contains('Apartment For')]
len(mu)  # 161
len(su)  # 339

# 卧室和浴室的数量和平方英尺需要解析，都在一列
su['propertyinfo_value']
# 检查没有包含'bd'或'Studio'的行数
len(su[~(su['propertyinfo_value'].str.contains('Studio') | su['propertyinfo_value'].str.contains('bd'))])  # 0
# 检查没有包含'ba'的行数
len(su[~(su['propertyinfo_value'].str.contains('ba'))])  # 6

# 选择拥有浴室的房源
no_baths = su[~(su['propertyinfo_value'].str.contains('ba'))]
# 排除缺失浴室信息的房源
sucln = su[~su.index.isin(no_baths.index)]


# 把类似'Studio • 1 ba • 550 sqft'的数据组合成数据框，不存在的数据用nan填充
def parse_info(row):
    if not 'sqft' in row:
        br, ba = row.split('•')[:2]
        sqft = np.nan
    else:
        br, ba, sqft = row.split('•')[:3]
    return pd.Series({'Beds': br, 'Baths': ba, 'Sqft': sqft})


# apply返回一个数据框，使每个公寓属性(propertyinfo_value)都成为单独的列，
attr = sucln['propertyinfo_value'].apply(parse_info)
# 去掉字符串(bd、ba、sqft)
attr_cln = attr.applymap(lambda x: x.strip().split(' ')[0] if isinstance(x, str) else np.nan)
# 合并原数据和属性数据
sujnd = sucln.join(attr_cln)


# 提取楼层信息：楼层数字后跟随一个字母
def parse_addy(r):
    so_zip = re.search(', NY(\d+)', r)
    so_flr = re.search('(?:APT|#)\s+(\d+)[A-Z]+,', r)
    if so_zip:
        zipc = so_zip.group(1)
    else:
        zipc = np.nan
    if so_flr:
        flr = so_flr.group(1)
    else:
        flr = np.nan
    return pd.Series({'Zip': zipc, 'Floor': flr})


flrzip = sujnd['routable_link/_text'].apply(parse_addy)
suf = sujnd.join(flrzip)
suf.T

# 只显示感兴趣的列
sudf = suf[['pricelarge_value_prices', 'Beds', 'Baths', 'Sqft', 'Floor', 'Zip']].copy()
# 重命名列名。inplace表示在修改源数据，默认false，设置为true之前要copy()一下，否则报错'A value is trying to be set on a copy of a slice from a DataFrame'
sudf.rename(columns={'pricelarge_value_prices': 'Rent'}, inplace=True)
# 重新索引
sudf.reset_index(drop=True, inplace=True)

'''
3. =========分析数据=========
'''
# 输出统计数据
sudf.describe()
# 需要把所有的数据转换为数值才能进行统计，把Studio替换为0
sudf.loc[:, 'Beds'] = sudf['Beds'].map(lambda x: 0 if 'Studio' in x else x)
# 输出每一列的数值类型，发现不都是数字
sudf.info()
# 调整数据类型
sudf.loc[:, 'Rent'] = sudf['Rent'].astype(int)
sudf.loc[:, 'Beds'] = sudf['Beds'].astype(int)
# 存在半间浴室，调整为float
sudf.loc[:, 'Baths'] = sudf['Baths'].astype(float)
# 存在NaN，需要float，但是要先将逗号替换掉
sudf.loc[:, 'Sqft'] = sudf['Sqft'].str.replace(',', '')
sudf.loc[:, 'Sqft'] = sudf['Sqft'].astype('float')
sudf.loc[:, 'Floor'] = sudf['Floor'].astype('float')
sudf.info()
sudf.describe()
# 发现318的楼层数大于1000，放弃这个房源
sudf = sudf.drop([318])
sudf.describe()
# 按照编码查看平均价格
sudf.pivot_table('Rent', 'Zip', 'Beds', aggfunc='mean')
# 根据房源数量进行透视
sudf.pivot_table('Rent', 'Zip', 'Beds', aggfunc='count')

# 可视化数据
# 目前的数据是基于邮政编码的，所以最好的可视化方法是使用热图
# 缺少包含两道三件卧室的公寓，缩减数据集
su_lt_two = sudf[sudf['Beds'] < 2]
map = folium.Map(location=[40.748817, -73.985428], zoom_start=3)

# 查看http://python-visualization.github.io/folium/docs-v0.5.0/quickstart.html#Getting-Started
# map.choropleth(
#     geo_data='./source_data/us-states.json',
#     columns=['Zip', 'Rent'],
#     key_on='feature.properties.postalCode',
#     # threshold_scale=[1700.00, 1900.00, 2100.00, 2300.00, 2500.00],
#     fill_color='YlGn',
#     fill_opacity=0.7,
#     line_opacity=0.2,
#     legend_name='Rent (%)',
# )
# map.save('nyc.html')

# 建模
# ~左边的Rent表示反应或因变量，右边的Zip和Beds表示独立或预测变量。表示想知道Zip和Beds如何影响Rent
f = 'Rent ~ Zip + Beds'
# 使用公式和数据框，得到一个数据框，X矩阵由预测变量组成，y向量由响应变量组成
y, X = patsy.dmatrices(f, su_lt_two, return_type='dataframe')
# .fit运行模型
results = sm.OLS(y, X).fit()
# 输出模型结果
# Adj R2为0.283，F值为1.21e-10，具有统计的显著性：仅仅用我是数量和邮政编码，就能够结实越三分之一的价格差异。
# 中间部分是模型中每个自变量的有关信息。从左到右为变量、变量在模型中的系数、标准误差、t统计量、t统计量的p值、95%得置信区间
results.summary()

# 预测
# 查看模型的输入
X.head()
# 创建自己的输入行进行预测。使用X矩阵的索引，并用零填充数据
to_pred_idx = X.iloc[0].index
to_pred_zeros = np.zeros(len(to_pred_idx))
tpdf = pd.DataFrame(to_pred_zeros, index=to_pred_idx, columns=['value'])
# 填入实际的值。对10009区域、包含一间卧室的公寓进行评估
# 对于线性回归，截距值必须设置为1，模型才能返回正确的统计值
tpdf.loc['Intercept'] = 1
tpdf.loc['Beds'] = 1
tpdf.loc['Zip[T.10009]'] = 1
# print(tpdf)
# 这时截距和10009邮编、卧室数量已设置为1了。已经将特征设置为了适当的值
# 运行预测，使用该模型返回一个预测：使用自己的输入值调用模型的predict方法，返回预测的值
results.predict(tpdf['value'])
# 改为两间卧室
tpdf['value'] = 0
tpdf.loc['Intercept'] = 1
tpdf.loc['Beds'] = 2
tpdf.loc['Zip[T.10009]'] = 1
results.predict(tpdf['value'])
