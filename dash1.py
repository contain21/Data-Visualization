import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import base64
from io import BytesIO
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


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
    knowledge_correct_counts['fully_correct_rate'] = knowledge_correct_counts[correct_state] / knowledge_correct_counts[
        'total_count']
    knowledge_correct_counts['partially_correct_rate'] = knowledge_correct_counts[partial_correct_states].sum(axis=1) / \
                                                         knowledge_correct_counts['total_count']
    knowledge_correct_counts['total_correct_rate'] = knowledge_correct_counts['fully_correct_rate'] + \
                                                     knowledge_correct_counts['partially_correct_rate']

    merged_scores = pd.merge(knowledge_scores_last, knowledge_scores, on='knowledge', suffixes=('_last', '_total'))
    merged_counts = pd.merge(knowledge_state_counts, knowledge_method_counts, on='knowledge',
                             suffixes=('_state', '_method'))
    merged_data = pd.merge(merged_scores, merged_counts, on='knowledge')
    merged_data = pd.merge(merged_data, knowledge_memory_time, on='knowledge')
    merged_data = pd.merge(merged_data, knowledge_correct_counts, on='knowledge')
    merged_data_knowledge = merged_data.reset_index()

    # 处理从属知识点数据
    sub_knowledge_scores_last = final_submission.groupby('sub_knowledge').agg(
        {'score_log': 'sum', 'score_title': 'sum'})
    sub_knowledge_scores_last['score_rate_last'] = sub_knowledge_scores_last['score_log'] / sub_knowledge_scores_last[
        'score_title']

    sub_knowledge_scores = student_data.groupby('sub_knowledge').agg({'score_log': 'sum', 'score_title': 'sum'})
    sub_knowledge_scores['score_rate'] = sub_knowledge_scores['score_log'] / sub_knowledge_scores['score_title']

    sub_knowledge_state_counts = student_data.groupby('sub_knowledge')['state'].value_counts().unstack(fill_value=0)
    sub_knowledge_method_counts = student_data.groupby('sub_knowledge')['method'].value_counts().unstack(fill_value=0)
    sub_knowledge_memory_time = student_data.groupby('sub_knowledge').agg({'memory': 'sum', 'timeconsume': 'sum'})

    sub_knowledge_correct_counts = student_data.groupby('sub_knowledge')['state'].value_counts().unstack(fill_value=0)

    sub_knowledge_correct_counts['total_count'] = sub_knowledge_correct_counts.sum(axis=1)
    sub_knowledge_correct_counts['fully_correct_rate'] = sub_knowledge_correct_counts[correct_state] / \
                                                         sub_knowledge_correct_counts['total_count']
    sub_knowledge_correct_counts['partially_correct_rate'] = sub_knowledge_correct_counts[partial_correct_states].sum(
        axis=1) / sub_knowledge_correct_counts['total_count']
    sub_knowledge_correct_counts['total_correct_rate'] = sub_knowledge_correct_counts['fully_correct_rate'] + \
                                                         sub_knowledge_correct_counts['partially_correct_rate']

    merged_scores = pd.merge(sub_knowledge_scores_last, sub_knowledge_scores, on='sub_knowledge',
                             suffixes=('_last', '_total'))
    merged_counts = pd.merge(sub_knowledge_state_counts, sub_knowledge_method_counts, on='sub_knowledge',
                             suffixes=('_state', '_method'))
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


def parallel_plot(df, cols, rank_attr, cmap='Spectral', spread=False, curved=0.1, curvedextend=0.05):
    colmap = plt.get_cmap(cmap)
    cols = cols + [rank_attr]

    fig, axes = plt.subplots(1, len(cols) - 1, sharey=False, figsize=(2 * len(cols) + 3, 5))
    valmat = np.ndarray(shape=(len(cols), len(df)))
    x = np.arange(0, len(cols), 1)
    ax_info = {}
    for i, col in enumerate(cols):
        vals = df[col]
        if (vals.dtype == float) & (len(np.unique(vals)) > 20):
            minval = np.min(vals)
            maxval = np.max(vals)
            rangeval = maxval - minval
            vals = np.true_divide(vals - minval, maxval - minval)
            nticks = 5
            tick_labels = [round(minval + i * (rangeval / nticks), 4) for i in range(nticks + 1)]
            ticks = [0 + i * (1.0 / nticks) for i in range(nticks + 1)]
            valmat[i] = vals
            ax_info[col] = [tick_labels, ticks]
        else:
            vals = vals.astype('category')
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
        ax.xaxis.set_major_locator(plt.FixedLocator([dim]))
        ax.yaxis.set_major_locator(plt.FixedLocator(ax_info[col][1]))
        if all(isinstance(label, float) for label in ax_info[col][0]):
            ax_info[col][0] = [f'{label:.3f}' for label in ax_info[col][0]]
        else:
            ax_info[col][0] = [int(label) for label in ax_info[col][0]]
        ax.set_yticklabels(ax_info[col][0])
        ax.set_xticklabels([cols[dim]])

    plt.subplots_adjust(wspace=0)
    norm = plt.Normalize(0, 1)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    cbar = plt.colorbar(sm, pad=0, ticks=ax_info[rank_attr][1], extend='both', extendrect=True, extendfrac=extendfrac,
                        ax=axes)
    cbar.ax.set_yticklabels(ax_info[rank_attr][0])
    fig.text(0.79, 0.93, rank_attr, fontsize=12, ha='center', va='center')

    return fig


def fig_to_base64(fig):
    buf = BytesIO()
    FigureCanvas(fig).print_png(buf)
    data = base64.b64encode(buf.getbuffer()).decode("utf8")
    plt.close(fig)
    return "data:image/png;base64,{}".format(data)


# Load your data
merged_knowledge_all = pd.read_csv('merged_knowledge_updated.csv')
merged_sub_knowledge_all = pd.read_csv('merged_sub_knowledge_updated.csv')

# Define the new column names dictionary
new_column_names = {
    'Method_5Q4KoXthUuYz3bvrTDFm': 'Method_5',
    'Method_BXr9AIsPQhwNvyGdZL57': 'Method_B',
    'Method_Cj9Ya2R7fZd6xs1q5mNQ': 'Method_C',
    'Method_gj1NLb4Jn7URf9K2kQPd': 'Method_g',
    'Method_m8vwGkEZc3TSW2xqYUoR': 'Method_m'
}

# Rename columns
merged_knowledge_all.rename(columns=new_column_names, inplace=True)
merged_sub_knowledge_all.rename(columns=new_column_names, inplace=True)

# Define the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Parallel Coordinates Plot"),
    dcc.Input(id='student-id-input', type='text', value='', placeholder='输入学生ID'),
    dcc.RadioItems(
        id='data-selector',
        options=[
            {'label': 'Knowledge', 'value': 'knowledge'},
            {'label': 'Sub Knowledge', 'value': 'sub_knowledge'}
        ],
        value='knowledge',
        labelStyle={'display': 'inline-block'}
    ),
    dcc.Dropdown(
        id='column-selector',
        options=[
            {'label': 'Columns Set 1', 'value': 'set1'},
            {'label': 'Columns Set 2', 'value': 'set2'},
            {'label': 'Columns Set 3', 'value': 'set3'}
        ],
        value='set1'
    ),
    html.Img(id='parallel-coordinates')
])


@app.callback(
    Output('parallel-coordinates', 'src'),
    [Input('student-id-input', 'value'),
     Input('data-selector', 'value'),
     Input('column-selector', 'value')]
)
def update_graph(student_id, data_selected, column_selected):
    if not student_id:

        if data_selected == 'knowledge':
            df = merged_knowledge_all
        else:
            df = merged_sub_knowledge_all

        if column_selected == 'set1':
            columns_to_plot = ['score_log', 'score_title', 'Absolutely_Correct',
                               'Partially_Correct',  'error']
        elif column_selected == 'set2':
            columns_to_plot = ['score_rate', 'fully_correct_rate',
                               'partially_correct_rate', 'total_correct_rate']
        else:  # column_selected == 'set3'
            columns_to_plot = ['Method_5', 'Method_B', 'Method_C', 'Method_g', 'Method_m',
                               'memory', 'timeconsume']

        fig = parallel_plot(df, columns_to_plot, 'knowledge' if data_selected == 'knowledge' else 'sub_knowledge')
        return fig_to_base64(fig)
    else:
        merged_knowledge, merged_sub_knowledge = get_student_data(student_id)

        if data_selected == 'knowledge':
            df = merged_knowledge
        else:
            df = merged_sub_knowledge

        if column_selected == 'set1':

            columns_to_plot = ['score_log_total', 'score_title_total', 'Absolutely_Correct_x', 'Partially_Correct_x',
                                'error_x']
        elif column_selected == 'set2':
            columns_to_plot = ['score_log_last', 'score_title_last','score_rate_last', 'fully_correct_rate', 'partially_correct_rate', 'total_correct_rate']
        else:
            columns_to_plot = ['Method_5', 'Method_B', 'Method_C', 'Method_g', 'Method_m', 'memory', 'timeconsume']

        fig = parallel_plot(df, columns_to_plot, 'knowledge' if data_selected == 'knowledge' else 'sub_knowledge')
        return fig_to_base64(fig)



if __name__ == '__main__':
    app.run_server(debug=True,port=8051)

