'''
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output, State

def get_student_data(student_id):
    merged_df = pd.read_csv('merged_info.csv')
    merged_df = merged_df[~merged_df['timeconsume'].isin(['--', '-'])]
    merged_df['timeconsume'] = pd.to_numeric(merged_df['timeconsume'])

    # 过滤出该学生的所有记录
    student_data = merged_df[merged_df['student_ID'] == student_id]
    # 根据题目ID排序，确保时间戳按照顺序排列
    student_data_sorted = student_data.sort_values(by=['title_ID', 'time'])
    final_submission = student_data_sorted.groupby('title_ID').last().reset_index()

    # 处理知识点数据
    knowledge_scores_last = final_submission.groupby('knowledge').agg({'score_log': 'sum', 'score_title': 'sum'})
    knowledge_scores_last['score_rate_last'] = knowledge_scores_last['score_log'] / knowledge_scores_last['score_title']

    knowledge_scores = student_data.groupby('knowledge').agg({'score_log': 'sum', 'score_title': 'sum'})
    knowledge_scores['score_rate'] = knowledge_scores['score_log'] / knowledge_scores['score_title']

    knowledge_state_counts = student_data.groupby('knowledge')['state'].value_counts().unstack(fill_value=0)
    knowledge_method_counts = student_data.groupby('knowledge')['method'].value_counts().unstack(fill_value=0)
    knowledge_memory_time = student_data.groupby('knowledge').agg({'memory': 'sum', 'timeconsume': 'sum'})

    correct_state = 'Absolutely_Correct'
    partial_correct_states = ['Partially_Correct']
    knowledge_correct_counts = student_data.groupby('knowledge')['state'].value_counts().unstack(fill_value=0)

    knowledge_correct_counts['total_count'] = knowledge_correct_counts.sum(axis=1)
    knowledge_correct_counts['fully_correct_rate'] = knowledge_correct_counts[correct_state] / knowledge_correct_counts['total_count']
    knowledge_correct_counts['partially_correct_rate'] = knowledge_correct_counts[partial_correct_states].sum(axis=1) / knowledge_correct_counts['total_count']
    knowledge_correct_counts['total_correct_rate'] = knowledge_correct_counts['fully_correct_rate'] + knowledge_correct_counts['partially_correct_rate']

    merged_scores = pd.merge(knowledge_scores_last, knowledge_scores, on='knowledge', suffixes=('_last', '_total'))
    merged_counts = pd.merge(knowledge_state_counts, knowledge_method_counts, on='knowledge', suffixes=('_state', '_method'))
    merged_data = pd.merge(merged_scores, merged_counts, on='knowledge')
    merged_data = pd.merge(merged_data, knowledge_memory_time, on='knowledge')
    merged_data = pd.merge(merged_data, knowledge_correct_counts, on='knowledge')
    merged_data_knowledge = merged_data.reset_index()

    # 处理从属知识点数据
    sub_knowledge_scores_last = final_submission.groupby('sub_knowledge').agg({'score_log': 'sum', 'score_title': 'sum'})
    sub_knowledge_scores_last['score_rate_last'] = sub_knowledge_scores_last['score_log'] / sub_knowledge_scores_last['score_title']

    sub_knowledge_scores = student_data.groupby('sub_knowledge').agg({'score_log': 'sum', 'score_title': 'sum'})
    sub_knowledge_scores['score_rate'] = sub_knowledge_scores['score_log'] / sub_knowledge_scores['score_title']

    sub_knowledge_state_counts = student_data.groupby('sub_knowledge')['state'].value_counts().unstack(fill_value=0)
    sub_knowledge_method_counts = student_data.groupby('sub_knowledge')['method'].value_counts().unstack(fill_value=0)
    sub_knowledge_memory_time = student_data.groupby('sub_knowledge').agg({'memory': 'sum', 'timeconsume': 'sum'})

    sub_knowledge_correct_counts = student_data.groupby('sub_knowledge')['state'].value_counts().unstack(fill_value=0)

    sub_knowledge_correct_counts['total_count'] = sub_knowledge_correct_counts.sum(axis=1)
    sub_knowledge_correct_counts['fully_correct_rate'] = sub_knowledge_correct_counts[correct_state] / sub_knowledge_correct_counts['total_count']
    sub_knowledge_correct_counts['partially_correct_rate'] = sub_knowledge_correct_counts[partial_correct_states].sum(axis=1) / sub_knowledge_correct_counts['total_count']
    sub_knowledge_correct_counts['total_correct_rate'] = sub_knowledge_correct_counts['fully_correct_rate'] + sub_knowledge_correct_counts['partially_correct_rate']

    merged_scores = pd.merge(sub_knowledge_scores_last, sub_knowledge_scores, on='sub_knowledge', suffixes=('_last', '_total'))
    merged_counts = pd.merge(sub_knowledge_state_counts, sub_knowledge_method_counts, on='sub_knowledge', suffixes=('_state', '_method'))
    merged_data = pd.merge(merged_scores, merged_counts, on='sub_knowledge')
    merged_data = pd.merge(merged_data, sub_knowledge_memory_time, on='sub_knowledge')
    merged_data = pd.merge(merged_data, sub_knowledge_correct_counts, on='sub_knowledge')
    merged_data_sub_knowledge = merged_data.reset_index()

    new_column_names = {
        'Method_5Q4KoXthUuYz3bvrTDFm': 'Method_5',
        'Method_BXr9AIsPQhwNvyGdZL57': 'Method_B',
        'Method_Cj9Ya2R7fZd6xs1q5mNQ': 'Method_C',
        'Method_gj1NLb4Jn7URf9K2kQPd': 'Method_g',
        'Method_m8vwGkEZc3TSW2xqYUoR': 'Method_m'
    }

    # Rename columns
    merged_data_knowledge.rename(columns=new_column_names, inplace=True)
    merged_data_sub_knowledge.rename(columns=new_column_names, inplace=True)
    return merged_data_knowledge, merged_data_sub_knowledge
# 读取CSV文件
df_knowledge = pd.read_csv('merged_knowledge_updated.csv')
df_sub_knowledge = pd.read_csv('merged_sub_knowledge_updated.csv')

# 数据归一化处理
scaler = MinMaxScaler()
df_knowledge_normalized = pd.DataFrame(scaler.fit_transform(df_knowledge.iloc[:, 1:]), columns=df_knowledge.columns[1:])
df_sub_knowledge_normalized = pd.DataFrame(scaler.fit_transform(df_sub_knowledge.iloc[:, 1:]), columns=df_sub_knowledge.columns[1:])

# 将知识点名称添加回归一化后的数据中
df_knowledge_normalized['knowledge'] = df_knowledge['knowledge']
df_sub_knowledge_normalized['sub_knowledge'] = df_sub_knowledge['sub_knowledge']

# 重命名列
new_column_names = {
    'Method_5Q4KoXthUuYz3bvrTDFm': 'Method_5',
    'Method_BXr9AIsPQhwNvyGdZL57': 'Method_B',
    'Method_Cj9Ya2R7fZd6xs1q5mNQ': 'Method_C',
    'Method_gj1NLb4Jn7URf9K2kQPd': 'Method_g',
    'Method_m8vwGkEZc3TSW2xqYUoR': 'Method_m'
}

df_knowledge_normalized.rename(columns=new_column_names, inplace=True)
df_sub_knowledge_normalized.rename(columns=new_column_names, inplace=True)



# 创建Dash应用程序
app = Dash(__name__)

app.layout = html.Div([
    html.Div([
        dcc.Input(id='student-id-input', type='text', placeholder='输入学生ID', debounce=True, style={'marginRight': '10px'}),
        dcc.RadioItems(
            id='knowledge-type',
            options=[
                {'label': '知识点', 'value': 'knowledge'},
                {'label': '从属知识点', 'value': 'sub_knowledge'}
            ],
            value='knowledge',
            inline=True
        )
    ], style={'marginBottom': '20px'}),
    dcc.Graph(id='radar-chart')
])

@app.callback(
    Output('radar-chart', 'figure'),
    [Input('student-id-input', 'value'),
     Input('knowledge-type', 'value')]
)
def update_radar_chart(student_id, knowledge_type):
    if student_id is None:
        # 默认显示整体数据
        if knowledge_type == 'knowledge':
            df = df_knowledge_normalized
            knowledge_points = df['knowledge']
            # 指标名称
            indicator_names = ['score_log', 'score_title', 'score_rate', 'Absolutely_Correct',
                               'Partially_Correct', 'Method_5', 'Method_B',
                               'Method_C', 'Method_g', 'Method_m',
                               'fully_correct_rate', 'partially_correct_rate']
        else:
            df = df_sub_knowledge_normalized
            knowledge_points = df['sub_knowledge']
            # 指标名称
            indicator_names = ['score_log', 'score_title', 'score_rate', 'Absolutely_Correct',
                               'Partially_Correct', 'Method_5', 'Method_B',
                               'Method_C', 'Method_g', 'Method_m',
                               'fully_correct_rate', 'partially_correct_rate']
    else:
        # 显示特定学生的数据
        df_knowledge, df_sub_knowledge = get_student_data(student_id)
        if knowledge_type == 'knowledge':
            df = df_knowledge
            knowledge_points = df['knowledge']
            # 指标名称
            indicator_names = ['score_log_last','score_title_last','score_rate_last','score_log_total',
                               'score_title_total','score_rate','Absolutely_Correct_x','Partially_Correct_x',
                               'Method_5', 'Method_B','Method_C', 'Method_g', 'Method_m',
                               'fully_correct_rate', 'partially_correct_rate']
        else:
            df = df_sub_knowledge
            knowledge_points = df['sub_knowledge']
            # 指标名称
            # 指标名称
            indicator_names = ['score_log_last', 'score_title_last', 'score_rate_last', 'score_log_total',
                               'score_title_total', 'score_rate', 'Absolutely_Correct_x', 'Partially_Correct_x',
                               'Method_5', 'Method_B', 'Method_C', 'Method_g', 'Method_m',
                               'fully_correct_rate', 'partially_correct_rate']

    data = df[indicator_names].values
    fig = go.Figure()

    for i in range(len(data)):
        fig.add_trace(go.Scatterpolar(
            r=data[i],
            theta=indicator_names,
            fill='toself',
            name=knowledge_points[i]
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
            )),
        showlegend=True,
        title='知识点雷达图' if knowledge_type == 'knowledge' else '从属知识点雷达图',
        font=dict(
            family='SimHei',
            size=15
        )
    )
    return fig



if __name__ == '__main__':
    app.run_server(debug=True,port=8051)
'''
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output, State

# 读取CSV文件
df_knowledge = pd.read_csv('merged_knowledge_updated.csv')
df_sub_knowledge = pd.read_csv('merged_sub_knowledge_updated.csv')
def get_student_data(student_id):
    merged_df = pd.read_csv('merged_info.csv')
    merged_df = merged_df[~merged_df['timeconsume'].isin(['--', '-'])]
    merged_df['timeconsume'] = pd.to_numeric(merged_df['timeconsume'])

    # 过滤出该学生的所有记录
    student_data = merged_df[merged_df['student_ID'] == student_id]
    # 根据题目ID排序，确保时间戳按照顺序排列
    student_data_sorted = student_data.sort_values(by=['title_ID', 'time'])
    final_submission = student_data_sorted.groupby('title_ID').last().reset_index()

    # 处理知识点数据
    knowledge_scores_last = final_submission.groupby('knowledge').agg({'score_log': 'sum', 'score_title': 'sum'})
    knowledge_scores_last['score_rate_last'] = knowledge_scores_last['score_log'] / knowledge_scores_last['score_title']

    knowledge_scores = student_data.groupby('knowledge').agg({'score_log': 'sum', 'score_title': 'sum'})
    knowledge_scores['score_rate'] = knowledge_scores['score_log'] / knowledge_scores['score_title']

    knowledge_state_counts = student_data.groupby('knowledge')['state'].value_counts().unstack(fill_value=0)
    knowledge_method_counts = student_data.groupby('knowledge')['method'].value_counts().unstack(fill_value=0)
    knowledge_memory_time = student_data.groupby('knowledge').agg({'memory': 'sum', 'timeconsume': 'sum'})

    correct_state = 'Absolutely_Correct'
    partial_correct_states = ['Partially_Correct']
    knowledge_correct_counts = student_data.groupby('knowledge')['state'].value_counts().unstack(fill_value=0)

    knowledge_correct_counts['total_count'] = knowledge_correct_counts.sum(axis=1)
    knowledge_correct_counts['fully_correct_rate'] = knowledge_correct_counts[correct_state] / knowledge_correct_counts['total_count']
    knowledge_correct_counts['partially_correct_rate'] = knowledge_correct_counts[partial_correct_states].sum(axis=1) / knowledge_correct_counts['total_count']
    knowledge_correct_counts['total_correct_rate'] = knowledge_correct_counts['fully_correct_rate'] + knowledge_correct_counts['partially_correct_rate']

    merged_scores = pd.merge(knowledge_scores_last, knowledge_scores, on='knowledge', suffixes=('_last', '_total'))
    merged_counts = pd.merge(knowledge_state_counts, knowledge_method_counts, on='knowledge', suffixes=('_state', '_method'))
    merged_data = pd.merge(merged_scores, merged_counts, on='knowledge')
    merged_data = pd.merge(merged_data, knowledge_memory_time, on='knowledge')
    merged_data = pd.merge(merged_data, knowledge_correct_counts, on='knowledge')
    merged_data_knowledge = merged_data.reset_index()

    # 处理从属知识点数据
    sub_knowledge_scores_last = final_submission.groupby('sub_knowledge').agg({'score_log': 'sum', 'score_title': 'sum'})
    sub_knowledge_scores_last['score_rate_last'] = sub_knowledge_scores_last['score_log'] / sub_knowledge_scores_last['score_title']

    sub_knowledge_scores = student_data.groupby('sub_knowledge').agg({'score_log': 'sum', 'score_title': 'sum'})
    sub_knowledge_scores['score_rate'] = sub_knowledge_scores['score_log'] / sub_knowledge_scores['score_title']

    sub_knowledge_state_counts = student_data.groupby('sub_knowledge')['state'].value_counts().unstack(fill_value=0)
    sub_knowledge_method_counts = student_data.groupby('sub_knowledge')['method'].value_counts().unstack(fill_value=0)
    sub_knowledge_memory_time = student_data.groupby('sub_knowledge').agg({'memory': 'sum', 'timeconsume': 'sum'})

    sub_knowledge_correct_counts = student_data.groupby('sub_knowledge')['state'].value_counts().unstack(fill_value=0)

    sub_knowledge_correct_counts['total_count'] = sub_knowledge_correct_counts.sum(axis=1)
    sub_knowledge_correct_counts['fully_correct_rate'] = sub_knowledge_correct_counts[correct_state] / sub_knowledge_correct_counts['total_count']
    sub_knowledge_correct_counts['partially_correct_rate'] = sub_knowledge_correct_counts[partial_correct_states].sum(axis=1) / sub_knowledge_correct_counts['total_count']
    sub_knowledge_correct_counts['total_correct_rate'] = sub_knowledge_correct_counts['fully_correct_rate'] + sub_knowledge_correct_counts['partially_correct_rate']

    merged_scores = pd.merge(sub_knowledge_scores_last, sub_knowledge_scores, on='sub_knowledge', suffixes=('_last', '_total'))
    merged_counts = pd.merge(sub_knowledge_state_counts, sub_knowledge_method_counts, on='sub_knowledge', suffixes=('_state', '_method'))
    merged_data = pd.merge(merged_scores, merged_counts, on='sub_knowledge')
    merged_data = pd.merge(merged_data, sub_knowledge_memory_time, on='sub_knowledge')
    merged_data = pd.merge(merged_data, sub_knowledge_correct_counts, on='sub_knowledge')
    merged_data_sub_knowledge = merged_data.reset_index()

    new_column_names = {
        'Method_5Q4KoXthUuYz3bvrTDFm': 'Method_5',
        'Method_BXr9AIsPQhwNvyGdZL57': 'Method_B',
        'Method_Cj9Ya2R7fZd6xs1q5mNQ': 'Method_C',
        'Method_gj1NLb4Jn7URf9K2kQPd': 'Method_g',
        'Method_m8vwGkEZc3TSW2xqYUoR': 'Method_m'
    }

    # Rename columns
    merged_data_knowledge.rename(columns=new_column_names, inplace=True)
    merged_data_sub_knowledge.rename(columns=new_column_names, inplace=True)
    return merged_data_knowledge, merged_data_sub_knowledge
# 数据归一化处理
scaler = MinMaxScaler()
df_knowledge_normalized = pd.DataFrame(scaler.fit_transform(df_knowledge.iloc[:, 1:]), columns=df_knowledge.columns[1:])
df_sub_knowledge_normalized = pd.DataFrame(scaler.fit_transform(df_sub_knowledge.iloc[:, 1:]), columns=df_sub_knowledge.columns[1:])

# 将知识点名称添加回归一化后的数据中
df_knowledge_normalized['knowledge'] = df_knowledge['knowledge']
df_sub_knowledge_normalized['sub_knowledge'] = df_sub_knowledge['sub_knowledge']

# 重命名列
new_column_names = {
    'Method_5Q4KoXthUuYz3bvrTDFm': 'Method_5',
    'Method_BXr9AIsPQhwNvyGdZL57': 'Method_B',
    'Method_Cj9Ya2R7fZd6xs1q5mNQ': 'Method_C',
    'Method_gj1NLb4Jn7URf9K2kQPd': 'Method_g',
    'Method_m8vwGkEZc3TSW2xqYUoR': 'Method_m'
}

df_knowledge_normalized.rename(columns=new_column_names, inplace=True)
df_sub_knowledge_normalized.rename(columns=new_column_names, inplace=True)

# 创建Dash应用程序
app = Dash(__name__)

# 设置应用程序布局
app.layout = html.Div([
    html.Div([
        dcc.Input(id='student-id-input', type='text', placeholder='输入学生ID', debounce=True, style={'marginRight': '10px'}),
        dcc.RadioItems(
            id='knowledge-type',
            options=[
                {'label': '知识点', 'value': 'knowledge'},
                {'label': '从属知识点', 'value': 'sub_knowledge'}
            ],
            value='knowledge',
            inline=True
        )
    ], style={'marginBottom': '20px'}),

    html.Div([
        dcc.Graph(id='radar-chart')
    ], style={'width': '60%', 'display': 'inline-block', 'verticalAlign': 'top', 'marginRight': '20px'}),

    html.Div([
        dcc.Graph(id='bar-line-chart')
    ], style={'width': '30%', 'display': 'inline-block', 'verticalAlign': 'top'})
])

# 回调函数：更新雷达图
@app.callback(
    Output('radar-chart', 'figure'),
    [Input('student-id-input', 'value'),
     Input('knowledge-type', 'value')]
)
def update_radar_chart(student_id, knowledge_type):
    if student_id is None:
        # 默认显示整体数据
        if knowledge_type == 'knowledge':
            df = df_knowledge_normalized
            knowledge_points = df['knowledge']
            # 指标名称
            indicator_names = ['score_log', 'score_title', 'score_rate', 'Absolutely_Correct',
                               'Partially_Correct', 'Method_5', 'Method_B',
                               'Method_C', 'Method_g', 'Method_m',
                               'fully_correct_rate', 'partially_correct_rate']
        else:
            df = df_sub_knowledge_normalized
            knowledge_points = df['sub_knowledge']
            # 指标名称
            indicator_names = ['score_log', 'score_title', 'score_rate', 'Absolutely_Correct',
                               'Partially_Correct', 'Method_5', 'Method_B',
                               'Method_C', 'Method_g', 'Method_m',
                               'fully_correct_rate', 'partially_correct_rate']
    else:
        # 显示特定学生的数据
        df_knowledge, df_sub_knowledge = get_student_data(student_id)
        if knowledge_type == 'knowledge':
            df = df_knowledge
            knowledge_points = df['knowledge']
            # 指标名称
            indicator_names = ['score_log_last','score_title_last','score_rate_last','score_log_total',
                               'score_title_total','score_rate','Absolutely_Correct_x','Partially_Correct_x',
                               'Method_5', 'Method_B','Method_C', 'Method_g', 'Method_m',
                               'fully_correct_rate', 'partially_correct_rate']
        else:
            df = df_sub_knowledge
            knowledge_points = df['sub_knowledge']
            # 指标名称
            indicator_names = ['score_log_last', 'score_title_last', 'score_rate_last', 'score_log_total',
                               'score_title_total', 'score_rate', 'Absolutely_Correct_x', 'Partially_Correct_x',
                               'Method_5', 'Method_B', 'Method_C', 'Method_g', 'Method_m',
                               'fully_correct_rate', 'partially_correct_rate']

    data = df[indicator_names].values
    fig = go.Figure()

    for i in range(len(data)):
        fig.add_trace(go.Scatterpolar(
            r=data[i],
            theta=indicator_names,
            fill='toself',
            name=knowledge_points[i]
        ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
            )),
        showlegend=True,
        title='知识点雷达图' if knowledge_type == 'knowledge' else '从属知识点雷达图',
        font=dict(
            family='SimHei',
            size=15
        )
    )
    return fig

# 读取CSV文件
df_knowledge_l = pd.read_csv('merged_knowledge_updated.csv')
df_sub_knowledge_l = pd.read_csv('merged_sub_knowledge_updated.csv')
# 回调函数：更新柱状图和折线图
@app.callback(
    Output('bar-line-chart', 'figure'),
    [Input('student-id-input', 'value'),
     Input('knowledge-type', 'value')]
)
def update_bar_line_chart(student_id, knowledge_type):
    if student_id is None:
        # 默认显示整体数据
        if knowledge_type == 'knowledge':
            df = df_knowledge_l
        else:
            df = df_sub_knowledge_l
    else:
        # 显示特定学生的数据
        df_knowledge, df_sub_knowledge = get_student_data(student_id)
        if knowledge_type == 'knowledge':
            df = df_knowledge
        else:
            df = df_sub_knowledge

    # 设置绘图所需的列
    knowledge_col = 'knowledge' if knowledge_type == 'knowledge' else 'sub_knowledge'
    bar_columns = ['fully_correct_rate', 'partially_correct_rate', 'total_correct_rate']
    line_column = 'score_rate'

    # 创建柱状图数据
    bar_traces = []
    for col in bar_columns:
        bar_traces.append(go.Bar(
            x=df[knowledge_col],
            y=df[col],
            name=col
        ))

    # 创建折线图数据
    line_trace = go.Scatter(
        x=df[knowledge_col],
        y=df[line_column],
        mode='lines+markers',
        name=line_column,
        yaxis='y2'  # 将折线图与第二个y轴关联
    )

    # 组合数据
    data = bar_traces + [line_trace]

    # 设置布局
    layout = go.Layout(
        title='Rates and Score over Knowledge' if knowledge_type == 'knowledge' else 'Rates and Score over Sub Knowledge',
        xaxis=dict(title='Knowledge' if knowledge_type == 'knowledge' else 'Sub Knowledge'),
        yaxis=dict(title='Rates'),
        yaxis2=dict(title='Score Rate', overlaying='y', side='right'),
        legend=dict(x=1.1, y=1)
    )

    # 创建图表
    fig = go.Figure(data=data, layout=layout)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=8057)
