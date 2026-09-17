import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
#答题高峰

# 假设数据保存在 'student_weekday_hourly_counts.csv' 文件中
data = pd.read_csv('student_weekday_hourly_counts.csv')


# 数据格式转换：将 'student_ID', 'weekday' 转换为索引，并转置时间列
# 这里需要聚合所有学生的数据以便绘制整体的热度图
heatmap_data = data.groupby(['weekday']).sum().drop(columns=['student_ID']).T
print(heatmap_data)
# 设置星期几标签
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
# 使用一个透明度渐变色方案从白色到红色

# 绘制热度图
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data,cmap='YlGnBu', linewidths=.5, annot=True, xticklabels=days_of_week)

# 设置图表标题和标签
plt.title('Weekly Hourly Problem Solving Count')
plt.xlabel('Weekday')
plt.ylabel('Hour')

# 显示热度图
plt.show()

# 输入要显示的学生ID
student_id = input("请输入学生ID: ")

# 提取特定学生的数据
student_data = data[data['student_ID'] == student_id]

# 数据格式转换：将 'weekday' 转换为索引，并转置时间列
# 这里需要聚合特定学生的数据以绘制热度图
heatmap_data = student_data.groupby(['weekday']).sum().drop(columns=['student_ID']).T

# 设置星期几标签
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# 绘制热度图
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap='YlGnBu', linewidths=.5, annot=True, xticklabels=days_of_week)

# 设置图表标题和标签
plt.title(f'Weekly Hourly Problem Solving Count for Student {student_id}')
plt.xlabel('Weekday')
plt.ylabel('Hour')

# 显示热度图
plt.show()

'''
#没有加面积
import plotly.graph_objects as go

# 数据
data = {
    'r8S3g': {
        'r8S3g_l0p5viby': ['Question_VgKw8PjY1FR6cm2QI9XW', 'Question_q7OpB2zCMmW9wS8uNt3H'],
        'r8S3g_n0m9rsw4': ['Question_q7OpB2zCMmW9wS8uNt3H', 'Question_fZrP3FJ4ebUogW9V7taS', 'Question_BW0ItEaymH3TkD6S15JF', 'Question_rvB9mVE6Kbd8jAY4NwPx']
    },
    't5V9e': {
        't5V9e_e1k6cixp': ['Question_3oPyUzDmQtcMfLpGZ0jW', 'Question_3MwAFlmNO8EKrpY5zjUd', 'Question_x2L7AqbMuTjCwPFy6vNr', 'Question_tgOjrpZLw4RdVzQx85h6', 'Question_s6VmP1G4UbEQWRYHK9Fd']
    },
    'm3D1v': {
        'm3D1v_r1d7fr3l': ['Question_h7pXNg80nJbw1C4kAPRm', 'Question_6RQj2gF3OeK5AmDvThUV', 'Question_4nHcauCQ0Y6Pm8DgKlLo', 'Question_TmKaGvfNoXYq4FZ2JrBu', 'Question_NixCn84GdK2tySa5rB1V', 'Question_n2BTxIGw1Mc3Zo6RLdUe', 'Question_QRm48lXxzdP7Tn1WgNOf', 'Question_pVKXjZn0BkSwYcsa7C31', 'Question_oCjnFLbIs4Uxwek9rBpu'],
        'm3D1v_v3d9is1x': ['Question_7NJzCXUPcvQF4Mkfh9Wr', 'Question_ZTbD7mxr2OUp8Fz6iNjy'],
        'm3D1v_t0v5ts9h': ['Question_Jr4Wz5jLqmN01KUwHa7g']
    },
    'y9W5d': {
        'y9W5d_c0w4mj5h': ['Question_QRm48lXxzdP7Tn1WgNOf', 'Question_pVKXjZn0BkSwYcsa7C31', 'Question_Ej5mBw9rsOUKkFycGvz2', 'Question_lU2wvHSZq7m43xiVroBc', 'Question_Mh4CZIsrEfxkP1wXtOYV', 'Question_62XbhBvJ8NUSnApgDL94', 'Question_x2Fy7rZ3SwYl9jMQkpOD', 'Question_UXqN1F7G3Sbldz02vZne'],
        'y9W5d_p8g6dgtv': ['Question_Ou3f2Wt9BqExm5DpN7Zk', 'Question_Az73sM0rHfWVKuc4X2kL'],
        'y9W5d_e2j7p95s': ['Question_EhVPdmlB31M8WKGqL0wc']
    },
    'k4W1c': {
        'k4W1c_h5r6nux7': ['Question_lU2wvHSZq7m43xiVroBc']
    },
    's8Y2f': {
        's8Y2f_v4x8by9j': ['Question_x2Fy7rZ3SwYl9jMQkpOD']
    },
    'g7R2j': {
        'g7R2j_e0v1yls8': ['Question_oCjnFLbIs4Uxwek9rBpu', 'Question_5fgqjSBwTPG7KUV3it6O', 'Question_X3wF8QlTyi4mZkDp9Kae', 'Question_xqlJkmRaP0otZcX4fK3W'],
        'g7R2j_j1g8gd3v': ['Question_YWXHr4G6Cl7bEm9iF2kQ']
    },
    'b3C9s': {
        'b3C9s_l4z6od7y': ['Question_bumGRTJ0c8p4v5D6eHZa', 'Question_hZ5wXofebmTlzKB1jNcP'],
        'b3C9s_j0v1yls8': ['Question_FNg8X9v5zcbB1tQrxHR3']
    }
}

# 构建Sunburst图数据
labels = []
parents = []

def add_to_lists(parent, children_dict):
    for key, value in children_dict.items():
        labels.append(key)
        parents.append(parent)
        if isinstance(value, dict):
            add_to_lists(key, value)
        else:
            for child in value:
                labels.append(child)
                parents.append(key)

# 构建第一层（根层）
for root, branches in data.items():
    labels.append(root)
    parents.append("")

    # 构建第二层和第三层
    add_to_lists(root, branches)

# 构建旭日图
fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    insidetextorientation='radial',
))

# 更新布局
fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0)
)

# 显示图表
fig.show()
'''
'''
import pandas as pd
import plotly.express as px

# 读取题目信息数据
title_info_df = pd.read_csv('Data_TitleInfo.csv')
data = pd.read_csv('student_combined_counts.csv')
# 构建层级结构
hierarchy = {}

for index, row in title_info_df.iterrows():
    knowledge_point = row['knowledge']
    sub_knowledge_point = row['sub_knowledge']
    title_id = row['title_ID']

    if knowledge_point not in hierarchy:
        hierarchy[knowledge_point] = {}
    if sub_knowledge_point not in hierarchy[knowledge_point]:
        hierarchy[knowledge_point][sub_knowledge_point] = []
    hierarchy[knowledge_point][sub_knowledge_point].append(title_id)
print(hierarchy)
'''
'''
import plotly.graph_objects as go
#加了面接（第一个人）
# 数据
data = {
    'r8S3g': {
        'r8S3g_l0p5viby': ['Question_VgKw8PjY1FR6cm2QI9XW', 'Question_q7OpB2zCMmW9wS8uNt3H'],
        'r8S3g_n0m9rsw4': ['Question_q7OpB2zCMmW9wS8uNt3H', 'Question_fZrP3FJ4ebUogW9V7taS', 'Question_BW0ItEaymH3TkD6S15JF', 'Question_rvB9mVE6Kbd8jAY4NwPx']
    },
    't5V9e': {
        't5V9e_e1k6cixp': ['Question_3oPyUzDmQtcMfLpGZ0jW', 'Question_3MwAFlmNO8EKrpY5zjUd', 'Question_x2L7AqbMuTjCwPFy6vNr', 'Question_tgOjrpZLw4RdVzQx85h6', 'Question_s6VmP1G4UbEQWRYHK9Fd']
    },
    'm3D1v': {
        'm3D1v_r1d7fr3l': ['Question_h7pXNg80nJbw1C4kAPRm', 'Question_6RQj2gF3OeK5AmDvThUV', 'Question_4nHcauCQ0Y6Pm8DgKlLo', 'Question_TmKaGvfNoXYq4FZ2JrBu', 'Question_NixCn84GdK2tySa5rB1V', 'Question_n2BTxIGw1Mc3Zo6RLdUe', 'Question_QRm48lXxzdP7Tn1WgNOf', 'Question_pVKXjZn0BkSwYcsa7C31', 'Question_oCjnFLbIs4Uxwek9rBpu'],
        'm3D1v_v3d9is1x': ['Question_7NJzCXUPcvQF4Mkfh9Wr', 'Question_ZTbD7mxr2OUp8Fz6iNjy'],
        'm3D1v_t0v5ts9h': ['Question_Jr4Wz5jLqmN01KUwHa7g']
    },
    'y9W5d': {
        'y9W5d_c0w4mj5h': ['Question_QRm48lXxzdP7Tn1WgNOf', 'Question_pVKXjZn0BkSwYcsa7C31', 'Question_Ej5mBw9rsOUKkFycGvz2', 'Question_lU2wvHSZq7m43xiVroBc', 'Question_Mh4CZIsrEfxkP1wXtOYV', 'Question_62XbhBvJ8NUSnApgDL94', 'Question_x2Fy7rZ3SwYl9jMQkpOD', 'Question_UXqN1F7G3Sbldz02vZne'],
        'y9W5d_p8g6dgtv': ['Question_Ou3f2Wt9BqExm5DpN7Zk', 'Question_Az73sM0rHfWVKuc4X2kL'],
        'y9W5d_e2j7p95s': ['Question_EhVPdmlB31M8WKGqL0wc']
    },
    'k4W1c': {
        'k4W1c_h5r6nux7': ['Question_lU2wvHSZq7m43xiVroBc']
    },
    's8Y2f': {
        's8Y2f_v4x8by9j': ['Question_x2Fy7rZ3SwYl9jMQkpOD']
    },
    'g7R2j': {
        'g7R2j_e0v1yls8': ['Question_oCjnFLbIs4Uxwek9rBpu', 'Question_5fgqjSBwTPG7KUV3it6O', 'Question_X3wF8QlTyi4mZkDp9Kae', 'Question_xqlJkmRaP0otZcX4fK3W'],
        'g7R2j_j1g8gd3v': ['Question_YWXHr4G6Cl7bEm9iF2kQ']
    },
    'b3C9s': {
        'b3C9s_l4z6od7y': ['Question_bumGRTJ0c8p4v5D6eHZa', 'Question_hZ5wXofebmTlzKB1jNcP'],
        'b3C9s_j0v1yls8': ['Question_FNg8X9v5zcbB1tQrxHR3']
    }
}

# 分数数据
scores = {
    'Question_3MwAFlmNO8EKrpY5zjUd': 23,
    'Question_3oPyUzDmQtcMfLpGZ0jW': 9,
    'Question_4nHcauCQ0Y6Pm8DgKlLo': 7,
    'Question_5fgqjSBwTPG7KUV3it6O': 22,
    'Question_62XbhBvJ8NUSnApgDL94': 1,
    'Question_6RQj2gF3OeK5AmDvThUV': 1,
    'Question_7NJzCXUPcvQF4Mkfh9Wr': 2,
    'Question_Az73sM0rHfWVKuc4X2kL': 4,
    'Question_BW0ItEaymH3TkD6S15JF': 8,
    'Question_EhVPdmlB31M8WKGqL0wc': 11,
    'Question_Ej5mBw9rsOUKkFycGvz2': 1,
    'Question_FNg8X9v5zcbB1tQrxHR3': 1,
    'Question_Jr4Wz5jLqmN01KUwHa7g': 5,
    'Question_Mh4CZIsrEfxkP1wXtOYV': 1,
    'Question_NixCn84GdK2tySa5rB1V': 1,
    'Question_Ou3f2Wt9BqExm5DpN7Zk': 14,
    'Question_QRm48lXxzdP7Tn1WgNOf': 4,
    'Question_TmKaGvfNoXYq4FZ2JrBu': 5,
    'Question_UXqN1F7G3Sbldz02vZne': 1,
    'Question_VgKw8PjY1FR6cm2QI9XW': 9,
    'Question_X3wF8QlTyi4mZkDp9Kae': 1,
    'Question_YWXHr4G6Cl7bEm9iF2kQ': 3,
    'Question_ZTbD7mxr2OUp8Fz6iNjy': 4,
    'Question_bumGRTJ0c8p4v5D6eHZa': 1,
    'Question_fZrP3FJ4ebUogW9V7taS': 13,
    'Question_h7pXNg80nJbw1C4kAPRm': 5,
    'Question_hZ5wXofebmTlzKB1jNcP': 2,
    'Question_lU2wvHSZq7m43xiVroBc': 8,
    'Question_n2BTxIGw1Mc3Zo6RLdUe': 3,
    'Question_oCjnFLbIs4Uxwek9rBpu': 8,
    'Question_pVKXjZn0BkSwYcsa7C31': 6,
    'Question_q7OpB2zCMmW9wS8uNt3H': 24,
    'Question_rvB9mVE6Kbd8jAY4NwPx': 4,
    'Question_s6VmP1G4UbEQWRYHK9Fd': 6,
    'Question_tgOjrpZLw4RdVzQx85h6': 4,
    'Question_x2Fy7rZ3SwYl9jMQkpOD': 12,
    'Question_x2L7AqbMuTjCwPFy6vNr': 9,
    'Question_xqlJkmRaP0otZcX4fK3W': 1
}

# 构建Sunburst图数据
labels = []
parents = []
values = []

def add_to_lists(parent, children_dict):
    for key, value in children_dict.items():
        labels.append(key)
        parents.append(parent)
        if isinstance(value, dict):
            add_to_lists(key, value)
        else:
            for child in value:
                labels.append(child)
                parents.append(key)
                values.append(scores.get(child, 0))

# 构建第一层（根层）
for root, branches in data.items():
    labels.append(root)
    parents.append("")
    values.append(0)  # 根层没有分数

    # 构建第二层和第三层
    add_to_lists(root, branches)

# 构建旭日图
fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    insidetextorientation='radial',
))

# 更新布局
fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0)
)

# 显示图表
fig.show()
'''

#总体情况
import pandas as pd
import plotly.graph_objects as go

# 读取CSV文件
df = pd.read_csv('student_combined_counts.csv')

# 计算每个问题的总分数
scores = df.iloc[:, 1:-23].sum().to_dict()
print(scores)
# 数据结构
data = {
    'r8S3g': {
        'r8S3g_l0p5viby': ['Question_VgKw8PjY1FR6cm2QI9XW', 'Question_q7OpB2zCMmW9wS8uNt3H'],
        'r8S3g_n0m9rsw4': ['Question_q7OpB2zCMmW9wS8uNt3H', 'Question_fZrP3FJ4ebUogW9V7taS', 'Question_BW0ItEaymH3TkD6S15JF', 'Question_rvB9mVE6Kbd8jAY4NwPx']
    },
    't5V9e': {
        't5V9e_e1k6cixp': ['Question_3oPyUzDmQtcMfLpGZ0jW', 'Question_3MwAFlmNO8EKrpY5zjUd', 'Question_x2L7AqbMuTjCwPFy6vNr', 'Question_tgOjrpZLw4RdVzQx85h6', 'Question_s6VmP1G4UbEQWRYHK9Fd']
    },
    'm3D1v': {
        'm3D1v_r1d7fr3l': ['Question_h7pXNg80nJbw1C4kAPRm', 'Question_6RQj2gF3OeK5AmDvThUV', 'Question_4nHcauCQ0Y6Pm8DgKlLo', 'Question_TmKaGvfNoXYq4FZ2JrBu', 'Question_NixCn84GdK2tySa5rB1V', 'Question_n2BTxIGw1Mc3Zo6RLdUe', 'Question_QRm48lXxzdP7Tn1WgNOf', 'Question_pVKXjZn0BkSwYcsa7C31', 'Question_oCjnFLbIs4Uxwek9rBpu'],
        'm3D1v_v3d9is1x': ['Question_7NJzCXUPcvQF4Mkfh9Wr', 'Question_ZTbD7mxr2OUp8Fz6iNjy'],
        'm3D1v_t0v5ts9h': ['Question_Jr4Wz5jLqmN01KUwHa7g']
    },
    'y9W5d': {
        'y9W5d_c0w4mj5h': ['Question_QRm48lXxzdP7Tn1WgNOf', 'Question_pVKXjZn0BkSwYcsa7C31', 'Question_Ej5mBw9rsOUKkFycGvz2', 'Question_lU2wvHSZq7m43xiVroBc', 'Question_Mh4CZIsrEfxkP1wXtOYV', 'Question_62XbhBvJ8NUSnApgDL94', 'Question_x2Fy7rZ3SwYl9jMQkpOD', 'Question_UXqN1F7G3Sbldz02vZne'],
        'y9W5d_p8g6dgtv': ['Question_Ou3f2Wt9BqExm5DpN7Zk', 'Question_Az73sM0rHfWVKuc4X2kL'],
        'y9W5d_e2j7p95s': ['Question_EhVPdmlB31M8WKGqL0wc']
    },
    'k4W1c': {
        'k4W1c_h5r6nux7': ['Question_lU2wvHSZq7m43xiVroBc']
    },
    's8Y2f': {
        's8Y2f_v4x8by9j': ['Question_x2Fy7rZ3SwYl9jMQkpOD']
    },
    'g7R2j': {
        'g7R2j_e0v1yls8': ['Question_oCjnFLbIs4Uxwek9rBpu', 'Question_5fgqjSBwTPG7KUV3it6O', 'Question_X3wF8QlTyi4mZkDp9Kae', 'Question_xqlJkmRaP0otZcX4fK3W'],
        'g7R2j_j1g8gd3v': ['Question_YWXHr4G6Cl7bEm9iF2kQ']
    },
    'b3C9s': {
        'b3C9s_l4z6od7y': ['Question_bumGRTJ0c8p4v5D6eHZa', 'Question_hZ5wXofebmTlzKB1jNcP'],
        'b3C9s_j0v1yls8': ['Question_FNg8X9v5zcbB1tQrxHR3']
    }
}

# 构建Sunburst图数据
labels = []
parents = []
values = []

def add_to_lists(parent, children_dict):
    for key, value in children_dict.items():
        labels.append(key)
        parents.append(parent)
        if isinstance(value, dict):
            add_to_lists(key, value)
        else:
            for child in value:
                labels.append(child)
                parents.append(key)
                values.append(scores.get(child, 0))

# 构建第一层（根层）
for root, branches in data.items():
    labels.append(root)
    parents.append("")
    values.append(0)  # 根层没有分数

    # 构建第二层和第三层
    add_to_lists(root, branches)

# 构建旭日图
fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    insidetextorientation='radial',
))

# 更新布局
fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0)
)

# 显示图表
fig.show()

'''
#输入id
import pandas as pd
import plotly.graph_objects as go

# 读取CSV文件
df = pd.read_csv('student_combined_counts.csv')
student_id=input('请输入学生id:')
# 筛选出指定学生的数据
student_data = df[df['student_ID'] == student_id]
# 计算每个问题的总分数
scores = student_data.iloc[:, 1:-23].sum().to_dict()
print(scores)
# 数据结构
data = {
    'r8S3g': {
        'r8S3g_l0p5viby': ['Question_VgKw8PjY1FR6cm2QI9XW', 'Question_q7OpB2zCMmW9wS8uNt3H'],
        'r8S3g_n0m9rsw4': ['Question_q7OpB2zCMmW9wS8uNt3H', 'Question_fZrP3FJ4ebUogW9V7taS', 'Question_BW0ItEaymH3TkD6S15JF', 'Question_rvB9mVE6Kbd8jAY4NwPx']
    },
    't5V9e': {
        't5V9e_e1k6cixp': ['Question_3oPyUzDmQtcMfLpGZ0jW', 'Question_3MwAFlmNO8EKrpY5zjUd', 'Question_x2L7AqbMuTjCwPFy6vNr', 'Question_tgOjrpZLw4RdVzQx85h6', 'Question_s6VmP1G4UbEQWRYHK9Fd']
    },
    'm3D1v': {
        'm3D1v_r1d7fr3l': ['Question_h7pXNg80nJbw1C4kAPRm', 'Question_6RQj2gF3OeK5AmDvThUV', 'Question_4nHcauCQ0Y6Pm8DgKlLo', 'Question_TmKaGvfNoXYq4FZ2JrBu', 'Question_NixCn84GdK2tySa5rB1V', 'Question_n2BTxIGw1Mc3Zo6RLdUe', 'Question_QRm48lXxzdP7Tn1WgNOf', 'Question_pVKXjZn0BkSwYcsa7C31', 'Question_oCjnFLbIs4Uxwek9rBpu'],
        'm3D1v_v3d9is1x': ['Question_7NJzCXUPcvQF4Mkfh9Wr', 'Question_ZTbD7mxr2OUp8Fz6iNjy'],
        'm3D1v_t0v5ts9h': ['Question_Jr4Wz5jLqmN01KUwHa7g']
    },
    'y9W5d': {
        'y9W5d_c0w4mj5h': ['Question_QRm48lXxzdP7Tn1WgNOf', 'Question_pVKXjZn0BkSwYcsa7C31', 'Question_Ej5mBw9rsOUKkFycGvz2', 'Question_lU2wvHSZq7m43xiVroBc', 'Question_Mh4CZIsrEfxkP1wXtOYV', 'Question_62XbhBvJ8NUSnApgDL94', 'Question_x2Fy7rZ3SwYl9jMQkpOD', 'Question_UXqN1F7G3Sbldz02vZne'],
        'y9W5d_p8g6dgtv': ['Question_Ou3f2Wt9BqExm5DpN7Zk', 'Question_Az73sM0rHfWVKuc4X2kL'],
        'y9W5d_e2j7p95s': ['Question_EhVPdmlB31M8WKGqL0wc']
    },
    'k4W1c': {
        'k4W1c_h5r6nux7': ['Question_lU2wvHSZq7m43xiVroBc']
    },
    's8Y2f': {
        's8Y2f_v4x8by9j': ['Question_x2Fy7rZ3SwYl9jMQkpOD']
    },
    'g7R2j': {
        'g7R2j_e0v1yls8': ['Question_oCjnFLbIs4Uxwek9rBpu', 'Question_5fgqjSBwTPG7KUV3it6O', 'Question_X3wF8QlTyi4mZkDp9Kae', 'Question_xqlJkmRaP0otZcX4fK3W'],
        'g7R2j_j1g8gd3v': ['Question_YWXHr4G6Cl7bEm9iF2kQ']
    },
    'b3C9s': {
        'b3C9s_l4z6od7y': ['Question_bumGRTJ0c8p4v5D6eHZa', 'Question_hZ5wXofebmTlzKB1jNcP'],
        'b3C9s_j0v1yls8': ['Question_FNg8X9v5zcbB1tQrxHR3']
    }
}

# 构建Sunburst图数据
labels = []
parents = []
values = []

def add_to_lists(parent, children_dict):
    for key, value in children_dict.items():
        labels.append(key)
        parents.append(parent)
        if isinstance(value, dict):
            add_to_lists(key, value)
        else:
            for child in value:
                labels.append(child)
                parents.append(key)
                values.append(scores.get(child, 0))

# 构建第一层（根层）
for root, branches in data.items():
    labels.append(root)
    parents.append("")
    values.append(0)  # 根层没有分数

    # 构建第二层和第三层
    add_to_lists(root, branches)

# 构建旭日图
fig = go.Figure(go.Sunburst(
    labels=labels,
    parents=parents,
    values=values,
    insidetextorientation='radial',
))

# 更新布局
fig.update_layout(
    margin=dict(t=0, l=0, r=0, b=0)
)

# 显示图表
fig.show()
'''
'''
import pandas as pd
import plotly.graph_objects as go

# 读取完全正确率数据
student_title_correct_rates = pd.read_csv('student_title_correct_rates.csv', index_col='student_ID')

# 读取部分正确率数据
student_title_partially_correct_rates = pd.read_csv('student_title_partially_correct_rates.csv', index_col='student_ID')

# 读取总正确率数据
student_title_any_correct_rates = pd.read_csv('student_title_any_correct_rates.csv', index_col='student_ID')

# 计算每个题目的平均值
mean_correct_rates = student_title_correct_rates.mean(axis=0)
mean_partially_correct_rates = student_title_partially_correct_rates.mean(axis=0)
mean_any_correct_rates = student_title_any_correct_rates.mean(axis=0)

# 创建绘图数据
fig = go.Figure()

# 添加完全正确率的柱状图
fig.add_trace(go.Bar(
    x=mean_correct_rates.values,
    y=mean_correct_rates.index,
    orientation='h',
    name='Mean Absolutely Correct Rate',
    marker=dict(color='blue')
))

# 添加部分正确率的柱状图
fig.add_trace(go.Bar(
    x=mean_partially_correct_rates.values,
    y=mean_partially_correct_rates.index,
    orientation='h',
    name='Mean Partially Correct Rate',
    marker=dict(color='orange')
))

# 添加总正确率的柱状图
fig.add_trace(go.Bar(
    x=mean_any_correct_rates.values,
    y=mean_any_correct_rates.index,
    orientation='h',
    name='Mean Any Correct Rate',
    marker=dict(color='green')
))

# 更新布局
fig.update_layout(
    barmode='group',
    title='Mean Correct Rates per Title',
    xaxis_title='Mean Correct Rate',
    yaxis_title='Title ID',
    legend_title='Legend'
)

# 显示图表
fig.show()

import pandas as pd
import plotly.graph_objects as go

# 读取完全正确率数据
student_title_correct_rates = pd.read_csv('student_title_correct_rates.csv', index_col='student_ID')

# 读取部分正确率数据
student_title_partially_correct_rates = pd.read_csv('student_title_partially_correct_rates.csv', index_col='student_ID')

# 读取总正确率数据
student_title_any_correct_rates = pd.read_csv('student_title_any_correct_rates.csv', index_col='student_ID')

# 输入要绘制的学生ID
student_id = input("请输入学生ID: ")

# 检查输入的学生ID是否在数据中
if student_id not in student_title_correct_rates.index:
    print("该学生ID不存在，请重新输入。")
    exit()

# 获取指定学生的数据
student_correct_rates = student_title_correct_rates.loc[student_id]
student_partially_correct_rates = student_title_partially_correct_rates.loc[student_id]
student_any_correct_rates = student_title_any_correct_rates.loc[student_id]

# 创建绘图数据
fig = go.Figure()

# 添加完全正确率的柱状图
fig.add_trace(go.Bar(
    x=student_correct_rates.values,
    y=student_correct_rates.index,
    orientation='h',
    name='Absolutely Correct Rate',
    marker=dict(color='blue')
))

# 添加部分正确率的柱状图
fig.add_trace(go.Bar(
    x=student_partially_correct_rates.values,
    y=student_partially_correct_rates.index,
    orientation='h',
    name='Partially Correct Rate',
    marker=dict(color='orange')
))

# 添加总正确率的柱状图
fig.add_trace(go.Bar(
    x=student_any_correct_rates.values,
    y=student_any_correct_rates.index,
    orientation='h',
    name='Any Correct Rate',
    marker=dict(color='green')
))

# 更新布局
fig.update_layout(
    barmode='group',
    title=f'Correct Rates for Student {student_id}',
    xaxis_title='Correct Rate',
    yaxis_title='Title ID',
    legend_title='Legend'
)

# 显示图表
fig.show()
'''

