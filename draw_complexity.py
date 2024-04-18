import numpy as np
import matplotlib.pyplot as plt
import math

# 定义数据
categories = ['S-Spectr', 'S-MIMO', 'L-Spectr', 'L-MIMO']
approach = ['SMT', 'MGDM', 'MF-MGDM']
sub_categories = ['working', 'backup']
values = [
    [[240.69/30/(49880.25/30+48159.0/30), 212.44/30/(49880.25/30+48159.0/30)], [7290.95/30/(49880.25/30+48159.0/30), 8427.62/30/(49880.25/30+48159.0/30)], [824.0/30/(49880.25/30+48159.0/30), 1017.13/30/(49880.25/30+48159.0/30)]],  # 类别A的四个数据，每个数据有两个子数据
    [[193.04/30/(43434.0/30+43434.0/30), 192.0/30/(43434.0/30+43434.0/30)], [194.84/30/(43434.0/30+43434.0/30), 217.43/30/(43434.0/30+43434.0/30)], [261.72/30/(43434.0/30+43434.0/30), 261.94/30/(43434.0/30+43434.0/30)]],  # 类别B的四个数据，每个数据有两个子数据
    [[170.0/25/(36342.0/25+36281.25/25), 185.6/25/(36342.0/25+36281.25/25)], [3553.0/25/(36342.0/25+36281.25/25), 2965.8/25/(36342.0/25+36281.25/25)], [0, 0]],  # 类别C的四个数据，每个数据有两个子数据
    [[168.06/25/(36281.25/25+36281.25/25), 184.02/25/(36281.25/25+36281.25/25)], [170.82/25/(36281.25/25+36281.25/25), 200.69/25/(36281.25/25+36281.25/25)], [0, 0]]   # 类别D的四个数据，每个数据有两个子数据
]
# 转换数据格式
values = np.array(values)
values = np.where(values != 0, 100 * (1.0 - values) * 0.5, values)
#print(100 * values)

# 对非零元素取对数
#values = np.where(values != 0, np.log10(100 * values), values)

# 确定每个柱的宽度和位置
bar_width = 0.15
index = np.arange(len(categories))

# 创建簇状柱状图
fig, ax = plt.subplots()

for i in range(len(approach)):
    data1 = [value[i][0] if len(value[i]) > 0 else 0 for value in values]
    data2 = [value[i][1] if len(value[i]) > 0 else 0 for value in values]
    ax.bar(index + i * bar_width, data1, bar_width, label=sub_categories[0] + ' ' + approach[i], alpha=0.7)
    ax.bar(index + i * bar_width, data2, bar_width, bottom=data1, label=sub_categories[1] + ' ' + approach[i], alpha=0.7)

# 添加标签
ax.set_xlabel('MIMO complexity', fontsize=14, fontname='Arial')
ax.set_ylabel('Reduction of MIMO', fontsize=14, fontname='Arial')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(categories, fontsize=12, fontname='Arial')
ax.tick_params(axis='y', labelsize=12)
#ax.set_ylim(0.4, 1.0)

# 添加网格线
ax.grid(True, linestyle='--', alpha=0.7)

# 设置图例位置和大小
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.15), ncol=len(approach), fontsize=8)  # 调整图例的位置和大小

# 显示图形
plt.tight_layout()
plt.show()
