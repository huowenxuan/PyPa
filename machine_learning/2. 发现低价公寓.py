import pandas as pd
import re
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

pd.set_option("display.max_columns", 30)
pd.set_option("display.max_colwidth", 100)
pd.set_option("display.precision", 3)

CSV_PATH = r'/Users/huowenxuan/Desktop/py/machine_learning/source_data/magic.csv'
df = pd.read_csv(CSV_PATH)
# 所有的列标题
df.columns
# 查看数据
df.head()
# 转置数据，并垂直显示
df.head().T
