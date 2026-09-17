'''import pandas as pd
import plotly.graph_objects as go

# 读取数据
data = pd.read_csv('student_weekday_hourly_counts.csv')

# 确保每一列的数据类型为整数，以防止数据类型问题
data.iloc[:, 2:] = data.iloc[:, 2:].apply(pd.to_numeric)

# 按星期几和小时聚合数据，求和
heatmap_data = data.groupby('weekday').sum().iloc[:, 0:25].drop(columns=['student_ID'])

# 转换星期几的数值为对应的字符串标签
weekday_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# 确保 weekday 的顺序正确
heatmap_data.index = weekday_labels
print(heatmap_data)

# 将数据转换为文本形式以在格子上显示
text_data = heatmap_data.values.astype(str)

# 绘制热度图
fig = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    text=text_data,
    colorscale='YlGnBu',  # 设置颜色映射
    hoverinfo='text',
    showscale=True,
    texttemplate="%{text}"  # 在每个格子上显示文本
))

# 设置图表布局
fig.update_layout(
    title='Total Number of Problems Solved by Time of Day and Day of Week',
    xaxis_title='Hour of Day',
    yaxis_title='Day of Week',
    xaxis_nticks=24,  # 设置 x 轴刻度数量，每小时一个刻度
    yaxis_nticks=7,   # 设置 y 轴刻度数量，每天一个刻度
    height=600,       # 设置图表高度
)

# 显示图表
fig.show()
'''
import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.graph_objects as go
import base64
import io

# 尝试读取 CSV 文件
try:
    data = pd.read_csv('student_weekday_hourly_counts.csv')
    combined_data = pd.read_csv('student_combined_counts.csv')
    correct_rates = pd.read_csv('student_title_correct_rates.csv', index_col='student_ID')
    partially_correct_rates = pd.read_csv('student_title_partially_correct_rates.csv', index_col='student_ID')
    any_correct_rates = pd.read_csv('student_title_any_correct_rates.csv', index_col='student_ID')
except FileNotFoundError as e:
    print(f"CSV 文件未找到: {e}")
    exit()

# 创建 Dash 应用
app = dash.Dash(__name__)

# 应用的布局
app.layout = html.Div([
    html.H1("Student Problem Solving Dashboard"),
    dcc.Input(id='student-id-input', type='text', placeholder='Enter Student ID'),
    html.Button(id='submit-button', n_clicks=0, children='Submit'),
    html.Div(id='output-container'),
    html.Div(id='sunburst-container'),
    html.Div(id='bar-chart-container')
])


# 辅助函数：创建热度图
def create_heatmap(heatmap_data, title):
    # 将数据转换为文本形式以在格子上显示
    text_data = heatmap_data.values.astype(str)

    # 绘制热度图
    fig = go.Figure(data=go.Heatmap(
        z=heatmap_data.values,
        x=heatmap_data.columns,
        y=heatmap_data.index,
        text=text_data,
        colorscale='YlGnBu',  # 设置颜色映射
        hoverinfo='text',
        showscale=True,
        texttemplate="%{text}"  # 在每个格子上显示文本
    ))

    # 设置图表布局
    fig.update_layout(
        title=title,
        xaxis_title='Hour of Day',
        yaxis_title='Day of Week',
        xaxis_nticks=24,  # 设置 x 轴刻度数量，每小时一个刻度
        yaxis_nticks=7,   # 设置 y 轴刻度数量，每天一个刻度
        height=600,       # 设置图表高度
    )

    return fig


# 辅助函数：创建 Sunburst 图
def create_sunburst(data, scores, title):
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

    for root, branches in data.items():
        labels.append(root)
        parents.append("")
        values.append(0)  # 根层没有分数

        add_to_lists(root, branches)

    fig = go.Figure(go.Sunburst(
        labels=labels,
        parents=parents,
        values=values,
        insidetextorientation='radial',
    ))

    fig.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
        title=title
    )

    return fig


# 辅助函数：创建 Bar 图
def create_bar_chart(correct_rates, partially_correct_rates, any_correct_rates, title):
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=correct_rates.values,
        y=correct_rates.index,
        orientation='h',
        name='Absolutely Correct Rate',
        marker=dict(color='blue')
    ))

    fig.add_trace(go.Bar(
        x=partially_correct_rates.values,
        y=partially_correct_rates.index,
        orientation='h',
        name='Partially Correct Rate',
        marker=dict(color='orange')
    ))

    fig.add_trace(go.Bar(
        x=any_correct_rates.values,
        y=any_correct_rates.index,
        orientation='h',
        name='Any Correct Rate',
        marker=dict(color='green')
    ))

    fig.update_layout(
        barmode='group',
        title=title,
        xaxis_title='Correct Rate',
        yaxis_title='Title ID',
        legend_title='Legend'
    )

    return fig


# 定义回调函数
@app.callback(
    [Output('output-container', 'children'),
     Output('sunburst-container', 'children'),
     Output('bar-chart-container', 'children')],
    [Input('submit-button', 'n_clicks'),
     Input('student-id-input', 'value')]
)
def update_output(n_clicks, student_id):
    if n_clicks > 0 and student_id:
        student_data = data[data['student_ID'] == student_id]
        if student_data.empty:
            return html.Div("No data found for the provided Student ID."), "", ""

        # 热度图
        heatmap_data = student_data.groupby(['weekday']).sum().drop(columns=['student_ID'])
        weekday_labels = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        heatmap_data.index = weekday_labels
        heatmap_fig = create_heatmap(heatmap_data, f'Weekly Hourly Problem Solving Count for Student {student_id}')

        # Sunburst 图
        student_combined_data = combined_data[combined_data['student_ID'] == student_id]
        scores = student_combined_data.iloc[:, 1:-23].sum().to_dict()
        sunburst_data = {
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
                'y9W5d_e2j7p95s': ['Question_EhVPdmlGnSxo7LJc43Mf', 'Question_vJke79qOs5cwVRn4aG6X']
            }
        }

        sunburst_fig = create_sunburst(sunburst_data, scores, f'Problem Solving Details for Student {student_id}')

        # Bar 图
        correct_rate_data = correct_rates.loc[student_id].dropna()
        partially_correct_rate_data = partially_correct_rates.loc[student_id].dropna()
        any_correct_rate_data = any_correct_rates.loc[student_id].dropna()
        bar_chart_fig = create_bar_chart(correct_rate_data, partially_correct_rate_data, any_correct_rate_data,
                                         f'Correct Rates for Student {student_id}')

        return dcc.Graph(figure=heatmap_fig), dcc.Graph(figure=sunburst_fig), dcc.Graph(figure=bar_chart_fig)
    return "", "", ""


# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True,port=8054)

