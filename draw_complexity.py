import numpy as np
import matplotlib.pyplot as plt

# 定义数据
categories = ['S-MIMO', 'S-Spectr', 'L-MIMO', 'L-Spectr']
approach = ['SMT', 'MGDM', 'Full-MIMO', 'MF-MGDM']
sub_categories = ['backup']
values = [
    [[6.359574468085106, 6.359574468085106], [6.359574468085106, 6.359574468085106], [1430.904255319149, 1430.904255319149], [8.640425531914895, 8.640425531914895]],
    [[6.359574468085106, 9.738297872340425], [151.0255319148936, 347.0851063829787], [1430.904255319149, 2254.7872340425533], [13.695744680851066, 44.078723404255314]],
    [[6.660465116279069, 7.31860465116279], [6.660465116279069, 7.344186046511628], [1434.2441860465117, 1434.2441860465117], [0, 0]],
    [[6.660465116279069, 11.097674418604651], [99.13488372093023, 229.87674418604652], [1434.2441860465117, 2371.9186046511627], [0, 0]]
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


ax.set_xlabel('MIMO complexity', fontsize=14, fontname='Arial')
ax.set_ylabel('MIMO Complexity backup per Tb/s', fontsize=14, fontname='Arial')
ax.set_xticks(index)
ax.set_xticklabels(categories, fontsize=12, fontname='Arial')
ax.tick_params(axis='y', labelsize=12)

# 使用对数坐标轴
ax.set_yscale('log')
ax.set_ylim(ymin=1)

# 添加网格线
ax.grid(True, linestyle='--', alpha=0.7)

# 设置图例位置和大小
ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.10), ncol=4, fontsize=9)

# 显示图形
plt.tight_layout()
plt.savefig('result\\Fig\\Complexity.png', dpi=2000)
plt.show()
