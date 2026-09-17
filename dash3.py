import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
'''
merged_df=pd.read_csv('merged_info.csv')
merged_df = merged_df[~merged_df['timeconsume'].isin(['--', '-'])]
merged_df['timeconsume'] = pd.to_numeric(merged_df['timeconsume'])

student_data_sorted = student_data.sort_values(by=['title_ID','time'])
final_submission = student_data_sorted.groupby('title_ID').last().reset_index()
knowledge_scores_last = final_submission.groupby('knowledge').agg({'score_log': 'sum', 'score_title': 'sum'})
knowledge_scores_last['score_rate_last'] = knowledge_scores_last['score_log'] / knowledge_scores_last['score_title']

# 提取时间段（小时）
# 1. 计算每个学生的总得分和题目总分
student_scores = merged_df.groupby('student_ID').agg(
    total_score=('score_log', 'sum'),
    total_title_score=('score_title', 'sum')
).reset_index()

# 2. 计算每个学生每个题目ID的做题数
student_title_counts = merged_df.groupby(['student_ID', 'title_ID']).size().unstack(fill_value=0)
student_title_counts  = student_title_counts.sum(axis=1).reset_index(name='total_title_count')

# 3. 计算每个学生每个知识点的做题数
student_knowledge_counts = merged_df.groupby(['student_ID', 'knowledge']).size().unstack(fill_value=0)
# 计算每个学生所有知识点的总做题数
student_knowledge_counts  = student_knowledge_counts.sum(axis=1).reset_index(name='total_knowledge_count')



# 4. 计算每个学生每个从属知识点的做题数
student_sub_knowledge_counts = merged_df.groupby(['student_ID', 'sub_knowledge']).size().unstack(fill_value=0)
student_sub_knowledge_counts  = student_sub_knowledge_counts.sum(axis=1).reset_index(name='total_sub_knowledge_count')



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



# 10. 计算每个学生在每个 title_ID 的答题正确率
# 假设 state 列中 '完全正确' 代表答对

merged_df['correct'] = merged_df['state'] == 'Absolutely_Correct'
student_title_correct_counts = merged_df.groupby(['student_ID', 'title_ID']).agg(
    total_count=('title_ID', 'size'),
    correct_count=('correct', 'sum')
).reset_index()
student_title_correct_counts['correct_rate'] = student_title_correct_counts['correct_count'] / student_title_correct_counts['total_count']
student_title_correct_rates = student_title_correct_counts.pivot(index='student_ID', columns='title_ID', values='correct_rate').fillna(0)
print(student_title_correct_rates)

merged_df['correct'] = merged_df['state'] == 'Absolutely_Correct'
merged_df['partially_correct'] = merged_df['state'] == 'Partially_Correct'
merged_df['any_correct'] = merged_df['correct'] | merged_df['partially_correct']
student_title_correct_counts = merged_df.groupby('student_ID').agg(
    total_count=('title_ID', 'size'),
    correct_count=('any_correct', 'sum')
).reset_index()
student_title_correct_counts['any_correct_rate'] = student_title_correct_counts['correct_count'] / student_title_correct_counts['total_count']

print(student_title_correct_counts)


# 11. 合并所有数据
student_summary = pd.merge(student_scores, student_title_counts, on='student_ID', how='left')
student_summary = pd.merge(student_summary, student_knowledge_counts, on='student_ID', how='left')
student_summary = pd.merge(student_summary, student_sub_knowledge_counts, on='student_ID', how='left')
student_summary = pd.merge(student_summary, student_hourly_counts, on='student_ID', how='left')
student_summary = pd.merge(student_summary, student_method_counts, on='student_ID', how='left')
student_summary = pd.merge(student_summary, student_memory_totals, on='student_ID', how='left')
student_summary = pd.merge(student_summary, student_timeconsume_totals, on='student_ID', how='left')
student_summary = pd.merge(student_summary, student_title_correct_counts, on='student_ID', how='left')

# 输出结果
print(student_summary)

# 保存结果到CSV文件
student_summary.to_csv('student_summary_new.csv', index=False)
'''
student_summary=pd.read_csv('student_summary_new.csv')
# 删除指定列
columns_to_drop = ['total_knowledge_count', 'total_sub_knowledge_count']
student_summary = student_summary.drop(columns=columns_to_drop)
print(student_summary)
