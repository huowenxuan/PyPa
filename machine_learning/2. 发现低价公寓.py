import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

pd.set_option("display.max_columns", 30)
pd.set_option("display.max_colwidth", 100)
pd.set_option("display.precision", 3)

'''
1. =========获取数据=========
'''
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
len(mu) # 161
len(su) # 339

# 卧室和浴室的数量和平方英尺需要解析，都在一列
su['propertyinfo_value']
# 检查没有包含'bd'或'Studio'的行数
len(su[~(su['propertyinfo_value'].str.contains('Studio') | su['propertyinfo_value'].str.contains('bd'))]) # 0
# 检查没有包含'ba'的行数
len(su[~(su['propertyinfo_value'].str.contains('ba'))]) # 6

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
