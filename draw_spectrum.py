import numpy as np
import matplotlib.pyplot as plt

# 定义数据
categories = ['S-Spectr', 'S-MIMO', 'L-Spectr', 'L-MIMO']
approach = ['SMT', 'MGDM', 'Full-MIMO', 'MF-MGDM']
sub_categories = ['working', 'backup']
values = [
    [[365.32/30, 26.0/30], [71.13/30, 24.46/30], [68.27/30, 24.78/30], [170.96/30, 26.0/30]],  # 类别A的四个数据，每个数据有两个子数据
    [[448.84/30, 25.84/30], [448.0/30, 26.37/30], [68.27/30, 24.83/30], [402.86/30, 50.7/30]],  # 类别B的四个数据，每个数据有两个子数据
    [[21.484375, 18.190625000000002], [12.91875, 11.66875], [21.265625, 17.646875000000003], [0, 0]],  # 类别C的四个数据，每个数据有两个子数据
    [[22.186666666666667, 18.606666666666667], [17.704166666666667, 8.340277777777778], [21.663333333333333, 17.996666666666664], [0, 0]]   # 类别D的四个数据，每个数据有两个子数据
]

# 确定每个柱的宽度和位置
bar_width = 0.15
index = np.arange(len(categories))

# 创建簇状柱状图
fig, ax = plt.subplots()

for i in range(len(categories)):
    data1 = [value[i][0] for value in values]
    data2 = [value[i][1] for value in values]
    ax.bar(index + i * bar_width, data1, bar_width, label=sub_categories[0] + ' ' + approach[i], alpha=0.7)
    ax.bar(index + i * bar_width, data2, bar_width, bottom=data1, label=sub_categories[1] + ' ' + approach[i], alpha=0.7)

# 添加标签
ax.set_xlabel('Spectrum occupation', fontsize=14, fontname='Arial')
ax.set_ylabel('Spectrum', fontsize=14, fontname='Arial')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(categories, fontsize=12, fontname='Arial')
ax.tick_params(axis='y', labelsize=12)

# 添加网格线
ax.grid(True, linestyle='--', alpha=0.7)

# 设置图例位置和大小
ax.legend(loc='upper center', bbox_to_anchor=(0.55, 1.1), ncol=len(categories), fontsize=8)  # 调整图例的位置和大小

# 显示图形
plt.tight_layout()
plt.show()
