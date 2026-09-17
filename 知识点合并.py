import pandas as pd

# 读取CSV文件
knowledge_scores = pd.read_csv('knowledge_scores.csv')
knowledge_state_counts = pd.read_csv('knowledge_state_counts.csv')
knowledge_method_counts = pd.read_csv('knowledge_method_counts.csv')
knowledge_memory_time = pd.read_csv('knowledge_memory_time.csv')
knowledge_correct_rates = pd.read_csv('knowledge_correct_rates.csv')

# 确保每个数据框的第一列是 'knowledge' 并设置为索引
knowledge_scores = knowledge_scores.set_index('knowledge')
knowledge_state_counts = knowledge_state_counts.set_index('knowledge')
knowledge_method_counts = knowledge_method_counts.set_index('knowledge')
knowledge_memory_time = knowledge_memory_time.set_index('knowledge')
knowledge_correct_rates = knowledge_correct_rates.set_index('knowledge')

# 转换 timeconsume 列为数值类型并从毫秒转换为小时
#knowledge_memory_time['timeconsume'] = pd.to_numeric(knowledge_memory_time['timeconsume'], errors='coerce')

# 合并数据框
# 合并数据框
merged_knowledge = knowledge_scores.join([knowledge_state_counts, knowledge_method_counts, knowledge_memory_time, knowledge_correct_rates], how='outer')
merged_knowledge=merged_knowledge.drop(columns=['�������'])
# 打印结果
print("合并后的数据框：")
print(merged_knowledge)

# 保存到CSV文件
merged_knowledge.to_csv('merged_knowledge.csv')
print("数据已保存到文件 'merged_knowledge.csv'")

# 读取CSV文件
sub_knowledge_scores = pd.read_csv('sub_knowledge_scores.csv')
sub_knowledge_state_counts = pd.read_csv('sub_knowledge_state_counts.csv')
sub_knowledge_method_counts = pd.read_csv('sub_knowledge_method_counts.csv')
sub_knowledge_memory_time = pd.read_csv('sub_knowledge_memory_time.csv')
sub_knowledge_correct_rates = pd.read_csv('sub_knowledge_correct_rates.csv')

# 确保每个数据框的第一列是 'sub_knowledge' 并设置为索引
sub_knowledge_scores = sub_knowledge_scores.set_index('sub_knowledge')
sub_knowledge_state_counts = sub_knowledge_state_counts.set_index('sub_knowledge')
sub_knowledge_method_counts = sub_knowledge_method_counts.set_index('sub_knowledge')
sub_knowledge_memory_time = sub_knowledge_memory_time.set_index('sub_knowledge')
sub_knowledge_correct_rates = sub_knowledge_correct_rates.set_index('sub_knowledge')

# 转换 timeconsume 列为数值类型并从毫秒转换为小时
#sub_knowledge_memory_time['timeconsume'] = pd.to_numeric(sub_knowledge_memory_time['timeconsume'], errors='coerce') / 3600000

# 合并数据框
merged_sub_knowledge = sub_knowledge_scores.join([sub_knowledge_state_counts, sub_knowledge_method_counts, sub_knowledge_memory_time, sub_knowledge_correct_rates], how='outer')
merged_sub_knowledge=merged_sub_knowledge.drop(columns=['�������'])
# 打印结果
print("合并后的数据框：")
print(merged_sub_knowledge)

# 保存到CSV文件
merged_sub_knowledge.to_csv('merged_sub_knowledge.csv')
print("数据已保存到文件 'merged_sub_knowledge.csv'")

# 读取CSV文件
merged_knowledge = pd.read_csv('merged_knowledge.csv')
merged_sub_knowledge = pd.read_csv('merged_sub_knowledge.csv')

# 将 'Absolutely_Error', 'Error1', 'Error2', 'Error3', 'Error4', 'Error5', 'Error6', 'Error7', 'Error8', 'Error9' 列相应加起来记为 'error' 列
merged_knowledge['error'] = merged_knowledge[['Absolutely_Error', 'Error1', 'Error2', 'Error3', 'Error4', 'Error5', 'Error6', 'Error7', 'Error8', 'Error9']].sum(axis=1)
merged_sub_knowledge['error'] = merged_sub_knowledge[['Absolutely_Error', 'Error1', 'Error2', 'Error3', 'Error4', 'Error5', 'Error6', 'Error7', 'Error8', 'Error9']].sum(axis=1)

# 删除 'Absolutely_Error', 'Error1', 'Error2', 'Error3', 'Error4', 'Error5', 'Error6', 'Error7', 'Error8', 'Error9' 列以及 '�������' 列
merged_knowledge = merged_knowledge.drop(columns=['Absolutely_Error', 'Error1', 'Error2', 'Error3', 'Error4', 'Error5', 'Error6', 'Error7', 'Error8', 'Error9'])
merged_sub_knowledge = merged_sub_knowledge.drop(columns=['Absolutely_Error', 'Error1', 'Error2', 'Error3', 'Error4', 'Error5', 'Error6', 'Error7', 'Error8', 'Error9'])

# 打印结果
print("处理后的 merged_knowledge 数据框：")
print(merged_knowledge)

print("处理后的 merged_sub_knowledge 数据框：")
print(merged_sub_knowledge)

# 保存到CSV文件
merged_knowledge.to_csv('merged_knowledge_updated.csv', index=False)
merged_sub_knowledge.to_csv('merged_sub_knowledge_updated.csv', index=False)

print("数据已保存到文件 'merged_knowledge_updated.csv' 和 'merged_sub_knowledge_updated.csv'")
