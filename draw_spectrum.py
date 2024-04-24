import numpy as np
import matplotlib.pyplot as plt

# 定义数据
categories = ['S-MIMO', 'S-Spectr', 'L-MIMO', 'L-Spectr']
approach = ['SMT', 'MGDM', 'Full-MIMO', 'MF-MGDM']
sub_categories = ['working', 'backup']
values = [
    [[15.057446808510639, 11.608510638297872], [15.057446808510639, 11.608510638297872], [2.4191489361702128, 1.7617021276595743], [13.519148936170213, 9.695744680851064]],  # 类别A的四个数据，每个数据有两个子数据
    [[12.363829787234042, 8.287234042553191], [3.0127659574468084, 1.1085106382978724], [2.4191489361702128, 0.9042553191489362], [7.648936170212766, 2.621276595744681]],  # 类别B的四个数据，每个数据有两个子数据
    [[17.77674418604651, 12.30232558139535], [17.77674418604651, 12.304651162790698], [2.8069767441860467, 1.9209302325581394], [0, 0]],  # 类别C的四个数据，每个数据有两个子数据
    [[14.309302325581394, 9.081395348837209], [4.641860465116279, 2.0558139534883724], [2.8069767441860467, 0.9744186046511628], [0, 0]]   # 类别D的四个数据，每个数据有两个子数据
]

# 处理数据中的零值
epsilon = 0
values = np.where(np.array(values) == 1, epsilon, np.array(values))

# 对数转换数据
values_log = np.zeros((4, 4))
for i in range(len(values)):
    for j in range(len(values[i])):
        if values[i][j][0] != 0 and values[i][j][1] != 0:
            values_log[i][j] = values[i][j][1]
            """values_log[i][j][1] = np.log2(values[i][j][1] + values[i][j][0]) - values_log[i][j][0]
            print(f"{i}, {j}, {values_log[i][j][0]}, {values_log[i][j][1]}")"""


# 确定每个柱的宽度和位置
bar_width = 0.15
index = np.arange(len(categories))

# 创建簇状柱状图
fig, ax = plt.subplots()

for i in range(len(categories)):
    data1 = [value[i] for value in values_log]
    #data2 = [value[i][1] for value in values_log]
    ax.bar(index + i * bar_width, data1, bar_width, label=sub_categories[0] + ' ' + approach[i], alpha=0.7)
    #ax.bar(index + i * bar_width, data2, bar_width, bottom=data1, label=sub_categories[1] + ' ' + approach[i], alpha=0.7)

# 添加标签
print(index + 1.5 * bar_width)
index = list(index)

for i in range(len(index)):
    if i < 2:
        index[i] += 1.5 * bar_width
    else:
        index[i] += bar_width
index = np.array(index)


ax.set_xlabel('Spectrum occupation', fontsize=14, fontname='Arial')
ax.set_ylabel('Spectrum occupation backup per Tb/s', fontsize=14, fontname='Arial')
ax.set_xticks(index)
ax.set_xticklabels(categories, fontsize=12, fontname='Arial')
ax.tick_params(axis='y', labelsize=12)

# 使用对数坐标轴
"""ax.set_yscale('log')
ax.set_ylim(ymin=1)"""

# 添加网格线
ax.grid(True, linestyle='--', alpha=0.7)

# 设置图例位置和大小
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.10), ncol=4, fontsize=9)

# 显示图形
plt.tight_layout()
plt.savefig('result\\Fig\\Spectrum', dpi=2000)
plt.show()
