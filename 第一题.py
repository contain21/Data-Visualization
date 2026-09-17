import matplotlib
from matplotlib import ticker
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline


def parallel_plot(df, cols, rank_attr, cmap='Spectral', spread=False, curved=0.1, curvedextend=0.05):
    colmap = matplotlib.colormaps.get_cmap(cmap)
    cols = cols + [rank_attr]

    fig, axes = plt.subplots(1, len(cols) - 1, sharey=False, figsize=(3 * len(cols) + 3, 5))  # 绘制多个子图
    valmat = np.ndarray(shape=(len(cols), len(df)))  # 定义需要绘制曲线的数组有df行，cols列
    x = np.arange(0, len(cols), 1)  # x 坐标范围
    ax_info = {}
    for i, col in enumerate(cols):  # 归一化数据
        vals = df[col]
        if (vals.dtype == float) & (len(np.unique(vals)) > 20):
            minval = np.min(vals)
            maxval = np.max(vals)
            rangeval = maxval - minval  # 区间长度
            vals = np.true_divide(vals - minval, maxval - minval)  # 归一化处理
            nticks = 5
            tick_labels = [round(minval + i * (rangeval / nticks), 4) for i in range(nticks + 1)]
            ticks = [0 + i * (1.0 / nticks) for i in range(nticks + 1)]
            valmat[i] = vals
            ax_info[col] = [tick_labels, ticks]
        else:
            vals = vals.astype('category')  # 假如是目录型
            cats = vals.cat.categories
            c_vals = vals.cat.codes
            minval = 0
            maxval = len(cats) - 1
            if maxval == 0:
                c_vals = 0.5
            else:
                c_vals = np.true_divide(c_vals - minval, maxval - minval)
            tick_labels = cats
            ticks = np.unique(c_vals)
            ax_info[col] = [tick_labels, ticks]
            if spread is not None:
                offset = np.arange(-1, 1, 2. / (len(c_vals))) * 2e-2
                np.random.shuffle(offset)
                c_vals = c_vals + offset
            valmat[i] = c_vals

    extendfrac = curvedextend if curved else 0.05
    for i, ax in enumerate(axes):
        for idx in range(valmat.shape[-1]):
            if curved:
                x_new = np.linspace(0, len(x), len(x) * 20)
                a_BSpline = make_interp_spline(x, valmat[:, idx], k=3, bc_type='clamped')
                y_new = a_BSpline(x_new)
                ax.plot(x_new, y_new, color=colmap(valmat[-1, idx]), alpha=0.5)
            else:
                ax.plot(x, valmat[:, idx], color=colmap(valmat[-1, idx]), alpha=0.5)
        ax.set_ylim(0 - extendfrac, 1 + extendfrac)
        ax.set_xlim(i, i + 1)

    for dim, (ax, col) in enumerate(zip(axes, cols)):
        ax.xaxis.set_major_locator(ticker.FixedLocator([dim]))
        ax.yaxis.set_major_locator(ticker.FixedLocator(ax_info[col][1]))
        # 如果刻度是小数，则将其格式化为三位小数
        if all(isinstance(label, float) for label in ax_info[col][0]):
            ax_info[col][0] = [f'{label:.3f}' for label in ax_info[col][0]]
        else:
            ax_info[col][0] = [int(label) for label in ax_info[col][0]]  # 否则保持整数标签不变
        ax.set_yticklabels(ax_info[col][0])
        ax.set_xticklabels([cols[dim]])

    plt.subplots_adjust(wspace=0)
    norm = matplotlib.colors.Normalize(0, 1)  # *axes[-1].get_ylim())
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cbar = plt.colorbar(sm, pad=0, ticks=ax_info[rank_attr][1], extend='both', extendrect=True, extendfrac=extendfrac,
                        ax=axes)
    cbar.ax.set_yticklabels(ax_info[rank_attr][0])
    # cbar.ax.set_xlabel(rank_attr)
    plt.show()
    # 在 colorbar 上方添加文本
    fig.text(0.79, 0.93, rank_attr, fontsize=12, ha='center', va='center')

    return x, valmat


# 知识点
merged_knowledge = pd.read_csv('merged_knowledge_updated.csv')
print(merged_knowledge.columns)
# 定义需要修改的列名字典
new_column_names = {
    'Method_5Q4KoXthUuYz3bvrTDFm': 'Method_5',
    'Method_BXr9AIsPQhwNvyGdZL57': 'Method_B',
    'Method_Cj9Ya2R7fZd6xs1q5mNQ': 'Method_C',
    'Method_gj1NLb4Jn7URf9K2kQPd': 'Method_g',
    'Method_m8vwGkEZc3TSW2xqYUoR': 'Method_m'
}

# 使用rename函数修改列名
merged_knowledge.rename(columns=new_column_names, inplace=True)
# 确定绘图所需的列
columns_to_plot1 = [ 'score_log', 'score_title', 'Absolutely_Correct',
                     'Partially_Correct', 'memory', 'timeconsume','error']

columns_to_plot2 = [ 'score_rate', 'fully_correct_rate',
                     'partially_correct_rate', 'total_correct_rate']
columns_to_plot3 = ['Method_5', 'Method_B',
                    'Method_C', 'Method_g', 'Method_m',
                    'memory', 'timeconsume']
# 绘制平行坐标图
parallel_plot(merged_knowledge, columns_to_plot1, 'knowledge')
parallel_plot(merged_knowledge, columns_to_plot2, 'knowledge')
parallel_plot(merged_knowledge, columns_to_plot3, 'knowledge')

#从属知识点
merged_sub_knowledge = pd.read_csv('merged_sub_knowledge_updated.csv')
# 定义需要修改的列名字典
new_column_names = {
    'Method_5Q4KoXthUuYz3bvrTDFm': 'Method_5',
    'Method_BXr9AIsPQhwNvyGdZL57': 'Method_B',
    'Method_Cj9Ya2R7fZd6xs1q5mNQ': 'Method_C',
    'Method_gj1NLb4Jn7URf9K2kQPd': 'Method_g',
    'Method_m8vwGkEZc3TSW2xqYUoR': 'Method_m'
}

# 使用rename函数修改列名
merged_sub_knowledge.rename(columns=new_column_names, inplace=True)
# 确定绘图所需的列
columns_to_plot1 = [ 'score_log', 'score_title', 'Absolutely_Correct',
                     'Partially_Correct', 'memory', 'timeconsume','error']

columns_to_plot2 = [ 'score_rate', 'fully_correct_rate',
                     'partially_correct_rate', 'total_correct_rate']
columns_to_plot3 = ['Method_5', 'Method_B',
                    'Method_C', 'Method_g', 'Method_m',
                    'memory', 'timeconsume']
# 绘制平行坐标图
parallel_plot(merged_sub_knowledge, columns_to_plot1, 'sub_knowledge')
parallel_plot(merged_sub_knowledge, columns_to_plot2, 'sub_knowledge')
parallel_plot(merged_sub_knowledge, columns_to_plot3, 'sub_knowledge')