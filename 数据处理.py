import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 导入学习者基本信息
students_df = pd.read_csv('Data_StudentInfo.csv')

# 导入题目基本信息
titles_df = pd.read_csv('Data_TitleInfo.csv')

# 读取已合并的日志记录
log_df = pd.read_csv('merged_log_title_converted.csv')
# 按student_ID合并数据

merged_df = pd.merge(log_df, students_df, on='student_ID', how='left',suffixes=('_log', '_title'))
# 保存合并后的数据
# 将 state 列中指定的值替换为 'error'
'''
error_states = ['Absolutely_Error', 'Error1', 'Error2', 'Error3', 'Error4', 'Error5', 'Error6', 'Error7', 'Error8', 'Error9']
merged_df['state'] = merged_df['state'].replace(error_states, 'error')
merged_df.to_csv('merged_info.csv', index=False)
'''
merged_df=pd.read_csv('merged_info.csv')
merged_df = merged_df[~merged_df['timeconsume'].isin(['--', '-'])]
merged_df['timeconsume'] = pd.to_numeric(merged_df['timeconsume'])
'''
# 输入要查询的学生ID 8b6d1125760bd3939b6e
student_id_to_search = input('请输入学生id：')
# 过滤出该学生的所有记录
student_data = merged_df[merged_df['student_ID'] == student_id_to_search]
# 输出该学生的所有记录
print(student_data)
#student_data.to_csv('stu1.csv', index=False)
# 根据题目ID排序，确保时间戳按照顺序排列
student_data_sorted = student_data.sort_values(by=['title_ID','time'])
final_submission = student_data_sorted.groupby('title_ID').last().reset_index()
knowledge_scores_last = final_submission.groupby('knowledge').agg({'score_log': 'sum', 'score_title': 'sum'})
knowledge_scores_last['score_rate_last'] = knowledge_scores_last['score_log'] / knowledge_scores_last['score_title']

# 排除 timeconsume 列中值为 '--' 和 '-' 的记录
student_data = student_data[~student_data['timeconsume'].isin(['--', '-'])]
student_data['timeconsume'] = pd.to_numeric(student_data['timeconsume'])
# 按知识点分组，并计算每个组的得分统计信息
knowledge_scores = student_data.groupby('knowledge').agg({'score_log': 'sum', 'score_title': 'sum'})
knowledge_scores['score_rate'] = (knowledge_scores['score_log'] / knowledge_scores['score_title'])
knowledge_state_counts = student_data.groupby('knowledge')['state'].value_counts().unstack(fill_value=0)
knowledge_method_counts = student_data.groupby('knowledge')['method'].value_counts().unstack(fill_value=0)
knowledge_memory_time = student_data.groupby('knowledge').agg({
    'memory': 'sum',
    'timeconsume': 'sum'
})

# 定义完全正确和部分正确的状态
correct_state = 'Absolutely_Correct'
partial_correct_states = ['Partially_Correct']

# 按知识点分组并统计各状态下的数量
knowledge_correct_counts = student_data.groupby('knowledge')['state'].value_counts().unstack(fill_value=0)

# 计算知识点完全正确率和部分正确率
knowledge_correct_counts['total_count'] = knowledge_correct_counts.sum(axis=1)
knowledge_correct_counts['fully_correct_rate'] = knowledge_correct_counts[correct_state] / knowledge_correct_counts['total_count']
knowledge_correct_counts['partially_correct_rate'] = knowledge_correct_counts[partial_correct_states].sum(axis=1) / knowledge_correct_counts['total_count']

# 计算总正确率
knowledge_correct_counts['total_correct_rate'] = knowledge_correct_counts['fully_correct_rate'] + knowledge_correct_counts['partially_correct_rate']

# 合并 knowledge_scores_last 和 knowledge_scores
merged_scores = pd.merge(knowledge_scores_last, knowledge_scores, on='knowledge', suffixes=('_last', '_total'))
# 合并 knowledge_state_counts 和 knowledge_method_counts
merged_counts = pd.merge(knowledge_state_counts, knowledge_method_counts, on='knowledge', suffixes=('_state', '_method'))
# 合并 merged_scores 和 merged_counts
merged_data = pd.merge(merged_scores, merged_counts, on='knowledge')
# 合并 knowledge_memory_time
merged_data = pd.merge(merged_data, knowledge_memory_time, on='knowledge')
merged_data = pd.merge(merged_data, knowledge_correct_counts, on='knowledge')
# 重新设置索引为 'knowledge'
merged_data = merged_data.reset_index()
# 输出合并后的数据
print(merged_data)
merged_data.to_csv('stumerged_knowledge.csv', index=False)


# 按从属知识点分组，并计算每个组的得分统计信息
sub_knowledge_scores_last = final_submission.groupby('sub_knowledge').agg({'score_log': 'sum', 'score_title': 'sum'})
sub_knowledge_scores_last['score_rate_last'] = sub_knowledge_scores_last['score_log'] / sub_knowledge_scores_last['score_title']
sub_knowledge_scores = student_data.groupby('sub_knowledge').agg({'score_log': 'sum', 'score_title': 'sum'})
sub_knowledge_scores['score_rate'] = (sub_knowledge_scores['score_log'] / sub_knowledge_scores['score_title'])
sub_knowledge_state_counts = student_data.groupby('sub_knowledge')['state'].value_counts().unstack(fill_value=0)
sub_knowledge_method_counts = student_data.groupby('sub_knowledge')['method'].value_counts().unstack(fill_value=0)
# 计算每个从属知识点的统计信息
sub_knowledge_memory_time = student_data.groupby('sub_knowledge').agg({
    'memory': 'sum',
    'timeconsume': 'sum'
})
# 按从属知识点分组并统计各状态下的数量
sub_knowledge_correct_counts = student_data.groupby('sub_knowledge')['state'].value_counts().unstack(fill_value=0)

# 计算从属知识点完全正确率和部分正确率
sub_knowledge_correct_counts['total_count'] = sub_knowledge_correct_counts.sum(axis=1)
sub_knowledge_correct_counts['fully_correct_rate'] = sub_knowledge_correct_counts[correct_state] / sub_knowledge_correct_counts['total_count']
sub_knowledge_correct_counts['partially_correct_rate'] = sub_knowledge_correct_counts[partial_correct_states].sum(axis=1) / sub_knowledge_correct_counts['total_count']

# 计算总正确率
sub_knowledge_correct_counts['total_correct_rate'] = sub_knowledge_correct_counts['fully_correct_rate'] + sub_knowledge_correct_counts['partially_correct_rate']


# 合并 knowledge_scores_last 和 knowledge_scores
merged_scores = pd.merge(sub_knowledge_scores_last, sub_knowledge_scores, on='sub_knowledge', suffixes=('_last', '_total'))
# 合并 knowledge_state_counts 和 knowledge_method_counts
merged_counts = pd.merge(sub_knowledge_state_counts, sub_knowledge_method_counts, on='sub_knowledge', suffixes=('_state', '_method'))
# 合并 merged_scores 和 merged_counts
merged_data = pd.merge(merged_scores, merged_counts, on='sub_knowledge')
# 合并 knowledge_memory_time
merged_data = pd.merge(merged_data, sub_knowledge_memory_time, on='sub_knowledge')
merged_data = pd.merge(merged_data, sub_knowledge_correct_counts, on='sub_knowledge')
# 重新设置索引为 'knowledge'
merged_data = merged_data.reset_index()
# 输出合并后的数据
print(merged_data)
merged_data.to_csv('stumerged_sub_knowledge.csv', index=False)
'''

'''
#学习者画像
# 提取时间段（小时）
# 1. 计算每个学生的总得分和题目总分
student_scores = merged_df.groupby('student_ID').agg(
    total_score=('score_log', 'sum'),
    total_title_score=('score_title', 'sum')
).reset_index()

# 2. 计算每个学生每个题目ID的做题数
student_title_counts = merged_df.groupby(['student_ID', 'title_ID']).size().unstack(fill_value=0)

# 3. 计算每个学生每个知识点的做题数
student_knowledge_counts = merged_df.groupby(['student_ID', 'knowledge']).size().unstack(fill_value=0)

# 4. 计算每个学生每个从属知识点的做题数
student_sub_knowledge_counts = merged_df.groupby(['student_ID', 'sub_knowledge']).size().unstack(fill_value=0)

# 5. 计算每个学生每个小时的做题数
merged_df['time'] = pd.to_datetime(merged_df['time'])
merged_df['hour'] = merged_df['time'].dt.hour
student_hourly_counts = merged_df.groupby(['student_ID', 'hour']).size().unstack(fill_value=0)

# 6. 计算每个学生在每个 method 的个数
student_method_counts = merged_df.groupby(['student_ID', 'method']).size().unstack(fill_value=0)

# 7. 计算每个学生的 memory 总数
student_memory_totals = merged_df.groupby('student_ID')['memory'].sum().reset_index()

# 8. 计算每个学生的 timeconsume 总数
student_timeconsume_totals = merged_df.groupby('student_ID')['timeconsume'].sum().reset_index()

# 9. 学生的性别、年龄、专业
student_info = merged_df[['student_ID', 'sex', 'age', 'major']].drop_duplicates()

# 10. 计算每个学生在每个 title_ID 的答题正确率
# 假设 state 列中 '完全正确' 代表答对    
merged_df['correct'] = merged_df['state'] == 'Absolutely_Correct'
student_title_correct_counts = merged_df.groupby(['student_ID', 'title_ID']).agg(
    total_count=('title_ID', 'size'),
    correct_count=('correct', 'sum')
).reset_index()
student_title_correct_counts['correct_rate'] = student_title_correct_counts['correct_count'] / student_title_correct_counts['total_count']
student_title_correct_rates = student_title_correct_counts.pivot(index='student_ID', columns='title_ID', values='correct_rate').fillna(0)

# 11. 合并所有数据
student_summary = pd.merge(student_scores, student_title_counts, on='student_ID', how='left')
student_summary = pd.merge(student_summary, student_knowledge_counts, on='student_ID', how='left')
student_summary = pd.merge(student_summary, student_sub_knowledge_counts, on='student_ID', how='left')
student_summary = pd.merge(student_summary, student_hourly_counts, on='student_ID', how='left')
student_summary = pd.merge(student_summary, student_method_counts, on='student_ID', how='left')
student_summary = pd.merge(student_summary, student_memory_totals, on='student_ID', how='left')
student_summary = pd.merge(student_summary, student_timeconsume_totals, on='student_ID', how='left')
student_summary = pd.merge(student_summary, student_info, on='student_ID', how='left')
student_summary = pd.merge(student_summary, student_title_correct_rates, on='student_ID', how='left')

# 输出结果
print(student_summary)

# 保存结果到CSV文件
student_summary.to_csv('student_summary.csv', index=False)

# 假设 merged_df 已经定义并包含所需数据
# 提取星期几和小时信息
merged_df['time'] = pd.to_datetime(merged_df['time'])
merged_df['weekday'] = merged_df['time'].dt.dayofweek  # 星期几，0 = Monday, 6 = Sunday
merged_df['hour'] = merged_df['time'].dt.hour

# 计算每个学生在每个星期几每个小时的做题数
student_weekday_hourly_counts = merged_df.groupby(['student_ID', 'weekday', 'hour']).size().unstack(fill_value=0).reset_index()

# 保存结果到CSV文件
student_weekday_hourly_counts.to_csv('student_weekday_hourly_counts.csv', index=False)

print(student_weekday_hourly_counts)

# 1. 计算每个学生每个题目ID的做题数
student_title_counts = merged_df.groupby(['student_ID', 'title_ID']).size().unstack(fill_value=0).reset_index()

# 2. 计算每个学生每个知识点的做题数
student_knowledge_counts = merged_df.groupby(['student_ID', 'knowledge']).size().unstack(fill_value=0).reset_index()

# 3. 计算每个学生每个从属知识点的做题数
student_sub_knowledge_counts = merged_df.groupby(['student_ID', 'sub_knowledge']).size().unstack(fill_value=0).reset_index()

# 4. 合并数据框
# 先合并 student_title_counts 和 student_knowledge_counts
merged_counts = pd.merge(student_title_counts, student_knowledge_counts, on='student_ID', how='outer', suffixes=('_title', '_knowledge'))

# 再合并 student_sub_knowledge_counts
merged_counts = pd.merge(merged_counts, student_sub_knowledge_counts, on='student_ID', how='outer')

# 5. 保存结果到CSV文件
merged_counts.to_csv('student_combined_counts.csv', index=False)

# 输出结果
print(merged_counts)'''
'''
merged_df['correct'] = merged_df['state'] == 'Absolutely_Correct'
merged_df['partially_correct'] = merged_df['state'] == 'Partially_Correct'
merged_df['any_correct'] = merged_df['correct'] | merged_df['partially_correct']

# 按学生和题目分组，并计算总答题次数、正确次数、部分正确次数和总正确次数
student_title_correct_counts = merged_df.groupby(['student_ID', 'title_ID']).agg(
    total_count=('title_ID', 'size'),
    correct_count=('correct', 'sum'),
    partially_correct_count=('partially_correct', 'sum'),
    any_correct_count=('any_correct', 'sum')
).reset_index()

# 计算正确率、部分正确率和总正确率
student_title_correct_counts['correct_rate'] = student_title_correct_counts['correct_count'] / student_title_correct_counts['total_count']
student_title_correct_counts['partially_correct_rate'] = student_title_correct_counts['partially_correct_count'] / student_title_correct_counts['total_count']
student_title_correct_counts['any_correct_rate'] = student_title_correct_counts['any_correct_count'] / student_title_correct_counts['total_count']

# 生成透视表，展示每个学生在每个题目上的正确率、部分正确率和总正确率
student_title_correct_rates = student_title_correct_counts.pivot(index='student_ID', columns='title_ID', values='correct_rate').fillna(0)
student_title_partially_correct_rates = student_title_correct_counts.pivot(index='student_ID', columns='title_ID', values='partially_correct_rate').fillna(0)
student_title_any_correct_rates = student_title_correct_counts.pivot(index='student_ID', columns='title_ID', values='any_correct_rate').fillna(0)

# 输出结果示例
print("Absolutely Correct Rates:")
print(student_title_correct_rates)

print("\nPartially Correct Rates:")
print(student_title_partially_correct_rates)

print("\nAny Correct Rates:")
print(student_title_any_correct_rates)

import pandas as pd
import plotly.graph_objects as go

# 假设 merged_df 已经被正确读取并包含以下列：student_ID, title_ID, state

# 创建新的列来表示不同的答题状态
merged_df['correct'] = merged_df['state'] == 'Absolutely_Correct'
merged_df['partially_correct'] = merged_df['state'] == 'Partially_Correct'
merged_df['any_correct'] = merged_df['correct'] | merged_df['partially_correct']

# 按学生和题目分组，并计算总答题次数、正确次数、部分正确次数和总正确次数
student_title_correct_counts = merged_df.groupby(['student_ID', 'title_ID']).agg(
    total_count=('title_ID', 'size'),
    correct_count=('correct', 'sum'),
    partially_correct_count=('partially_correct', 'sum'),
    any_correct_count=('any_correct', 'sum')
).reset_index()

# 计算正确率、部分正确率和总正确率
student_title_correct_counts['correct_rate'] = student_title_correct_counts['correct_count'] / student_title_correct_counts['total_count']
student_title_correct_counts['partially_correct_rate'] = student_title_correct_counts['partially_correct_count'] / student_title_correct_counts['total_count']
student_title_correct_counts['any_correct_rate'] = student_title_correct_counts['any_correct_count'] / student_title_correct_counts['total_count']

# 生成透视表
student_title_correct_rates = student_title_correct_counts.pivot(index='student_ID', columns='title_ID', values='correct_rate').fillna(0)
student_title_partially_correct_rates = student_title_correct_counts.pivot(index='student_ID', columns='title_ID', values='partially_correct_rate').fillna(0)
student_title_any_correct_rates = student_title_correct_counts.pivot(index='student_ID', columns='title_ID', values='any_correct_rate').fillna(0)

# 保存完全正确率数据到 CSV
student_title_correct_rates.to_csv('student_title_correct_rates.csv')

# 保存部分正确率数据到 CSV
student_title_partially_correct_rates.to_csv('student_title_partially_correct_rates.csv')

# 保存总正确率数据到 CSV
student_title_any_correct_rates.to_csv('student_title_any_correct_rates.csv')
'''
import pandas as pd

# 假设 merged_df 包含 'state', 'knowledge_point_ID' 等列
# 创建新的列以标记正确和部分正确的回答
merged_df['correct'] = merged_df['state'] == 'Absolutely_Correct'
merged_df['partially_correct'] = merged_df['state'] == 'Partially_Correct'
merged_df['any_correct'] = merged_df['correct'] | merged_df['partially_correct']

# 按知识点分组，并计算总答题次数、正确次数、部分正确次数和总正确次数
knowledge_point_correct_counts = merged_df.groupby(['student_ID','knowledge']).agg(
    total_count=('knowledge', 'size'),
    correct_count=('correct', 'sum'),
    partially_correct_count=('partially_correct', 'sum'),
    any_correct_count=('any_correct', 'sum')
).reset_index()

# 计算正确率、部分正确率和总正确率
knowledge_point_correct_counts['correct_rate'] = knowledge_point_correct_counts['correct_count'] / knowledge_point_correct_counts['total_count']
knowledge_point_correct_counts['partially_correct_rate'] = knowledge_point_correct_counts['partially_correct_count'] / knowledge_point_correct_counts['total_count']
knowledge_point_correct_counts['any_correct_rate'] = knowledge_point_correct_counts['any_correct_count'] / knowledge_point_correct_counts['total_count']

# 创建透视表
knowledge_correct_rates = knowledge_point_correct_counts.pivot(index='student_ID', columns='knowledge', values='correct_rate').fillna(0)
knowledge_partially_correct_rates = knowledge_point_correct_counts.pivot(index='student_ID', columns='knowledge', values='partially_correct_rate').fillna(0)
knowledge_any_correct_rates = knowledge_point_correct_counts.pivot(index='student_ID', columns='knowledge', values='any_correct_rate').fillna(0)

# 保存三个数据到 CSV 文件
knowledge_correct_rates.to_csv('knowledge_correct_rates.csv')
knowledge_partially_correct_rates.to_csv('knowledge_partially_correct_rates.csv')
knowledge_any_correct_rates.to_csv('knowledge_any_correct_rates.csv')

#sub_knowledge
merged_df['correct'] = merged_df['state'] == 'Absolutely_Correct'
merged_df['partially_correct'] = merged_df['state'] == 'Partially_Correct'
merged_df['any_correct'] = merged_df['correct'] | merged_df['partially_correct']

# 按知识点分组，并计算总答题次数、正确次数、部分正确次数和总正确次数
sub_knowledge_point_correct_counts = merged_df.groupby(['student_ID','sub_knowledge']).agg(
    total_count=('sub_knowledge', 'size'),
    correct_count=('correct', 'sum'),
    partially_correct_count=('partially_correct', 'sum'),
    any_correct_count=('any_correct', 'sum')
).reset_index()

# 计算正确率、部分正确率和总正确率
sub_knowledge_point_correct_counts['correct_rate'] = sub_knowledge_point_correct_counts['correct_count'] / sub_knowledge_point_correct_counts['total_count']
sub_knowledge_point_correct_counts['partially_correct_rate'] = sub_knowledge_point_correct_counts['partially_correct_count'] / sub_knowledge_point_correct_counts['total_count']
sub_knowledge_point_correct_counts['any_correct_rate'] = sub_knowledge_point_correct_counts['any_correct_count'] / sub_knowledge_point_correct_counts['total_count']

# 创建透视表
sub_knowledge_correct_rates = sub_knowledge_point_correct_counts.pivot(index='student_ID', columns='sub_knowledge', values='correct_rate').fillna(0)
sub_knowledge_partially_correct_rates = sub_knowledge_point_correct_counts.pivot(index='student_ID', columns='sub_knowledge', values='partially_correct_rate').fillna(0)
sub_knowledge_any_correct_rates = sub_knowledge_point_correct_counts.pivot(index='student_ID', columns='sub_knowledge', values='any_correct_rate').fillna(0)

# 保存三个数据到 CSV 文件
sub_knowledge_correct_rates.to_csv('sub_knowledge_correct_rates.csv')
sub_knowledge_partially_correct_rates.to_csv('sub_knowledge_partially_correct_rates.csv')
sub_knowledge_any_correct_rates.to_csv('sub_knowledge_any_correct_rates.csv')




