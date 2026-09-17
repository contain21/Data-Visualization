
'''

import pandas as pd
import plotly.graph_objects as go
import plotly.colors as pc

# 读取并处理 student_title_correct_rates.csv
student_title_correct_rates = pd.read_csv('student_title_correct_rates.csv', index_col='student_ID')
student_title_correct_rates_mean = student_title_correct_rates.mean()

# 读取并处理 knowledge_correct_rates.csv
knowledge_correct_rates = pd.read_csv('knowledge_correct_rates.csv', index_col='student_ID')
knowledge_correct_rates_mean = knowledge_correct_rates.mean()

# 读取并处理 sub_knowledge_correct_rates.csv
sub_knowledge_correct_rates = pd.read_csv('sub_knowledge_correct_rates.csv', index_col='student_ID')
sub_knowledge_correct_rates_mean = sub_knowledge_correct_rates.mean()

# 定义节点数据
data = {
    'r8S3g': {
        'r8S3g_l0p5viby': ['Question_VgKw8PjY1FR6cm2QI9XW', 'Question_q7OpB2zCMmW9wS8uNt3H'],
        'r8S3g_n0m9rsw4': ['Question_q7OpB2zCMmW9wS8uNt3H', 'Question_fZrP3FJ4ebUogW9V7taS',
                           'Question_BW0ItEaymH3TkD6S15JF', 'Question_rvB9mVE6Kbd8jAY4NwPx']
    },
    't5V9e': {
        't5V9e_e1k6cixp': ['Question_3oPyUzDmQtcMfLpGZ0jW', 'Question_3MwAFlmNO8EKrpY5zjUd',
                           'Question_x2L7AqbMuTjCwPFy6vNr', 'Question_tgOjrpZLw4RdVzQx85h6',
                           'Question_s6VmP1G4UbEQWRYHK9Fd']
    },
    'm3D1v': {
        'm3D1v_r1d7fr3l': ['Question_h7pXNg80nJbw1C4kAPRm', 'Question_6RQj2gF3OeK5AmDvThUV',
                           'Question_4nHcauCQ0Y6Pm8DgKlLo', 'Question_TmKaGvfNoXYq4FZ2JrBu',
                           'Question_NixCn84GdK2tySa5rB1V', 'Question_n2BTxIGw1Mc3Zo6RLdUe',
                           'Question_QRm48lXxzdP7Tn1WgNOf', 'Question_pVKXjZn0BkSwYcsa7C31',
                           'Question_oCjnFLbIs4Uxwek9rBpu'],
        'm3D1v_v3d9is1x': ['Question_7NJzCXUPcvQF4Mkfh9Wr', 'Question_ZTbD7mxr2OUp8Fz6iNjy'],
        'm3D1v_t0v5ts9h': ['Question_Jr4Wz5jLqmN01KUwHa7g']
    },
    'y9W5d': {
        'y9W5d_c0w4mj5h': ['Question_QRm48lXxzdP7Tn1WgNOf', 'Question_pVKXjZn0BkSwYcsa7C31',
                           'Question_Ej5mBw9rsOUKkFycGvz2', 'Question_lU2wvHSZq7m43xiVroBc',
                           'Question_Mh4CZIsrEfxkP1wXtOYV', 'Question_62XbhBvJ8NUSnApgDL94',
                           'Question_x2Fy7rZ3SwYl9jMQkpOD', 'Question_UXqN1F7G3Sbldz02vZne'],
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
        'g7R2j_e0v1yls8': ['Question_oCjnFLbIs4Uxwek9rBpu', 'Question_5fgqjSBwTPG7KUV3it6O',
                           'Question_X3wF8QlTyi4mZkDp9Kae', 'Question_xqlJkmRaP0otZcX4fK3W'],
        'g7R2j_j1g8gd3v': ['Question_YWXHr4G6Cl7bEm9iF2kQ']
    },
    'b3C9s': {
        'b3C9s_l4z6od7y': ['Question_bumGRTJ0c8p4v5D6eHZa', 'Question_hZ5wXofebmTlzKB1jNcP'],
        'b3C9s_j0v1yls8': ['Question_FNg8X9v5zcbB1tQrxHR3']
    }
}

# 准备桑基图所需的节点和链接
nodes = []
links = {'source': [], 'target': [], 'value': []}
node_indices = {}
node_thickness = []

# 辅助函数：添加节点并返回其索引，同时记录节点的厚度
def add_node(node):
    if node not in node_indices:
        node_indices[node] = len(nodes)
        nodes.append(node)
        thickness_value = (student_title_correct_rates_mean.get(node, 0)
                           or knowledge_correct_rates_mean.get(node, 0)
                           or sub_knowledge_correct_rates_mean.get(node, 0))
        node_thickness.append(thickness_value)
    return node_indices[node]

# 解析数据
for key, sub_dict in data.items():
    parent_index = add_node(key)
    for sub_key, questions in sub_dict.items():
        child_index = add_node(sub_key)
        links['source'].append(parent_index)
        links['target'].append(child_index)
        links['value'].append(len(questions))
        for question in questions:
            question_index = add_node(question)
            links['source'].append(child_index)
            links['target'].append(question_index)
            links['value'].append(1)

# 计算节点颜色
colorscale = [[0, 'rgb(0, 0, 255)'], [0.5, 'rgb(0, 255, 0)'], [1, 'rgb(255, 0, 0)']]
node_colors = []

min_thickness = min(node_thickness)
max_thickness = max(node_thickness)

for thickness in node_thickness:
    normalized_value = (thickness - min_thickness) / (max_thickness - min_thickness) if max_thickness > min_thickness else 0.5
    color_value = pc.find_intermediate_color(colorscale[0][1], colorscale[2][1], normalized_value, colortype='rgb')
    node_colors.append(color_value)

# 更新节点标签以包含厚度信息
node_labels = [f'{node} ({thickness:.2f})' for node, thickness in zip(nodes, node_thickness)]

# 创建桑基图
fig = go.Figure(go.Sankey(
    node=dict(
        pad=15,
        thickness=20,  # 动态调整厚度
        line=dict(color="black", width=0.5),
        label=node_labels,  # 使用更新后的标签
        color=node_colors,
        customdata=node_thickness,
        hovertemplate='Node %{label}<br>Mean Value: %{customdata:.2f}',
    ),
    link=dict(
        source=links['source'],
        target=links['target'],
        value=links['value']
    )
))

# 更新布局
fig.update_layout(title_text="Sankey Diagram", font_size=10)

# 显示图形
fig.show()
'''
import pandas as pd
import plotly.graph_objects as go
import plotly.colors as pc
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# 初始化Dash应用
app = dash.Dash(__name__)

# 读取数据文件
correct_rates_files = {
    'correct': {
        'student_title': 'student_title_correct_rates.csv',
        'knowledge': 'knowledge_correct_rates.csv',
        'sub_knowledge': 'sub_knowledge_correct_rates.csv'
    },
    'partially_correct': {
        'student_title': 'student_title_partially_correct_rates.csv',
        'knowledge': 'knowledge_partially_correct_rates.csv',
        'sub_knowledge': 'sub_knowledge_partially_correct_rates.csv'
    },
    'any_correct': {
        'student_title': 'student_title_any_correct_rates.csv',
        'knowledge': 'knowledge_any_correct_rates.csv',
        'sub_knowledge': 'sub_knowledge_any_correct_rates.csv'
    }
}

# 定义节点数据
data = {
    'r8S3g': {
        'r8S3g_l0p5viby': ['Question_VgKw8PjY1FR6cm2QI9XW', 'Question_q7OpB2zCMmW9wS8uNt3H'],
        'r8S3g_n0m9rsw4': ['Question_q7OpB2zCMmW9wS8uNt3H', 'Question_fZrP3FJ4ebUogW9V7taS',
                           'Question_BW0ItEaymH3TkD6S15JF', 'Question_rvB9mVE6Kbd8jAY4NwPx']
    },
    't5V9e': {
        't5V9e_e1k6cixp': ['Question_3oPyUzDmQtcMfLpGZ0jW', 'Question_3MwAFlmNO8EKrpY5zjUd',
                           'Question_x2L7AqbMuTjCwPFy6vNr', 'Question_tgOjrpZLw4RdVzQx85h6',
                           'Question_s6VmP1G4UbEQWRYHK9Fd']
    },
    'm3D1v': {
        'm3D1v_r1d7fr3l': ['Question_h7pXNg80nJbw1C4kAPRm', 'Question_6RQj2gF3OeK5AmDvThUV',
                           'Question_4nHcauCQ0Y6Pm8DgKlLo', 'Question_TmKaGvfNoXYq4FZ2JrBu',
                           'Question_NixCn84GdK2tySa5rB1V', 'Question_n2BTxIGw1Mc3Zo6RLdUe',
                           'Question_QRm48lXxzdP7Tn1WgNOf', 'Question_pVKXjZn0BkSwYcsa7C31',
                           'Question_oCjnFLbIs4Uxwek9rBpu'],
        'm3D1v_v3d9is1x': ['Question_7NJzCXUPcvQF4Mkfh9Wr', 'Question_ZTbD7mxr2OUp8Fz6iNjy'],
        'm3D1v_t0v5ts9h': ['Question_Jr4Wz5jLqmN01KUwHa7g']
    },
    'y9W5d': {
        'y9W5d_c0w4mj5h': ['Question_QRm48lXxzdP7Tn1WgNOf', 'Question_pVKXjZn0BkSwYcsa7C31',
                           'Question_Ej5mBw9rsOUKkFycGvz2', 'Question_lU2wvHSZq7m43xiVroBc',
                           'Question_Mh4CZIsrEfxkP1wXtOYV', 'Question_62XbhBvJ8NUSnApgDL94',
                           'Question_x2Fy7rZ3SwYl9jMQkpOD', 'Question_UXqN1F7G3Sbldz02vZne'],
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
        'g7R2j_e0v1yls8': ['Question_oCjnFLbIs4Uxwek9rBpu', 'Question_5fgqjSBwTPG7KUV3it6O',
                           'Question_X3wF8QlTyi4mZkDp9Kae', 'Question_xqlJkmRaP0otZcX4fK3W'],
        'g7R2j_j1g8gd3v': ['Question_YWXHr4G6Cl7bEm9iF2kQ']
    },
    'b3C9s': {
        'b3C9s_l4z6od7y': ['Question_bumGRTJ0c8p4v5D6eHZa', 'Question_hZ5wXofebmTlzKB1jNcP'],
        'b3C9s_j0v1yls8': ['Question_FNg8X9v5zcbB1tQrxHR3']
    }
}

# 辅助函数：添加节点并返回其索引，同时记录节点的厚度
def add_node(node, node_indices, nodes, node_thickness, mean_values):
    if node not in node_indices:
        node_indices[node] = len(nodes)
        nodes.append(node)
        thickness_value = mean_values.get(node, 0)
        node_thickness.append(thickness_value)
    return node_indices[node]

# 准备桑基图数据
def prepare_sankey_data(student_id='', rate_type='correct'):
    nodes = []
    links = {'source': [], 'target': [], 'value': []}
    node_indices = {}
    node_thickness = []

    # 加载相应的文件
    student_title_correct_rates = pd.read_csv(correct_rates_files[rate_type]['student_title'], index_col='student_ID')
    knowledge_correct_rates = pd.read_csv(correct_rates_files[rate_type]['knowledge'], index_col='student_ID')
    sub_knowledge_correct_rates = pd.read_csv(correct_rates_files[rate_type]['sub_knowledge'], index_col='student_ID')

    student_title_correct_rates_mean = student_title_correct_rates.mean()
    knowledge_correct_rates_mean = knowledge_correct_rates.mean()
    sub_knowledge_correct_rates_mean = sub_knowledge_correct_rates.mean()

    if student_id:
        student_data = pd.concat([
            student_title_correct_rates.loc[student_id],
            knowledge_correct_rates.loc[student_id],
            sub_knowledge_correct_rates.loc[student_id]
        ])
        mean_values = student_data
    else:
        mean_values = pd.concat([
            student_title_correct_rates_mean,
            knowledge_correct_rates_mean,
            sub_knowledge_correct_rates_mean
        ])

    # 解析数据
    for key, sub_dict in data.items():
        parent_index = add_node(key, node_indices, nodes, node_thickness, mean_values)
        for sub_key, questions in sub_dict.items():
            child_index = add_node(sub_key, node_indices, nodes, node_thickness, mean_values)
            links['source'].append(parent_index)
            links['target'].append(child_index)
            links['value'].append(len(questions))
            for question in questions:
                question_index = add_node(question, node_indices, nodes, node_thickness, mean_values)
                links['source'].append(child_index)
                links['target'].append(question_index)
                links['value'].append(1)

    return nodes, node_thickness, links

# 创建桑基图
def create_sankey_figure(student_id='', rate_type='correct'):
    nodes, node_thickness, links = prepare_sankey_data(student_id, rate_type)

    colorscale = [[0, 'rgb(0, 0, 255)'], [0.5, 'rgb(0, 255, 0)'], [1, 'rgb(255, 0, 0)']]
    node_colors = []

    min_thickness = min(node_thickness)
    max_thickness = max(node_thickness)

    for thickness in node_thickness:
        normalized_value = (thickness - min_thickness) / (max_thickness - min_thickness) if max_thickness > min_thickness else 0.5
        color_value = pc.find_intermediate_color(colorscale[0][1], colorscale[2][1], normalized_value, colortype='rgb')
        node_colors.append(color_value)

    node_labels = [f'{node} ({thickness:.2f})' for node, thickness in zip(nodes, node_thickness)]

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=node_labels,
            color=node_colors,
            customdata=node_thickness,
            hovertemplate='Node %{label}<br>Mean Value: %{customdata:.2f}',
        ),
        link=dict(
            source=links['source'],
            target=links['target'],
            value=links['value']
        )
    ))

    fig.update_layout(title_text="Sankey Diagram", font_size=10)
    return fig

# 定义布局
app.layout = html.Div([
    html.H1("Parallel Coordinates Plot"),
    dcc.Input(id='student-id-input', type='text', value='', placeholder='输入学生ID'),
    dcc.RadioItems(
        id='data-selector',
        options=[
            {'label': 'Correct Rate', 'value': 'correct'},
            {'label': 'Partially Correct Rate', 'value': 'partially_correct'},
            {'label': 'Any Correct Rate', 'value': 'any_correct'}
        ],
        value='correct',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Graph(id='sankey-plot'),
])

# 定义回调函数
@app.callback(
    Output('sankey-plot', 'figure'),
    [Input('student-id-input', 'value'),
     Input('data-selector', 'value')]
)
def update_sankey_plot(student_id, rate_type):
    return create_sankey_figure(student_id, rate_type)

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True,port=8055)


