import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pyvis.network import Network
# 导入数据
titles_df = pd.read_csv('Data_TitleInfo.csv')

# 找出重复的 title_ID
duplicated_titles = titles_df[titles_df.duplicated('title_ID', keep=False)]

# 显示重复的 title_ID 及其记录
print("重复的 title_ID 及其记录：")
print(duplicated_titles)

# 找出不重复的title_ID
unique_title_IDs = titles_df['title_ID'].unique()

# 找出不重复的knowledge
unique_knowledge = titles_df['knowledge'].unique()

unique_sub_knowledge = titles_df['sub_knowledge'].unique()

# 打印不重复的title_ID数量
print(f"不重复的title_ID数量: {len(unique_title_IDs)}")

# 打印不重复的knowledge数量
print(f"不重复的knowledge数量: {len(unique_knowledge)}")
print(f"不重复的sub_knowledge数量: {len(unique_sub_knowledge)}")

# 如果需要列出所有不重复的记录，可以使用以下代码：
print("不重复的title_ID记录: ", unique_title_IDs)
print("不重复的knowledge记录: ", unique_knowledge)
print("不重复的sub_knowledge记录: ", unique_sub_knowledge)

# 创建一个有向图
G = nx.DiGraph()

# 遍历每一行，将题目、从属知识点和知识点添加到图中
for index, row in titles_df.iterrows():
    title_id = row['title_ID']
    knowledge_points = row['knowledge'].split(',')  # 分割多个知识点
    sub_knowledge_points = row['sub_knowledge'].split(',')  # 分割多个从属知识点

    G.add_node(title_id, color='red', title='题目')  # 添加题目节点，颜色为红色

    for skp in sub_knowledge_points:
        G.add_node(skp, color='green', title='从属知识点')  # 添加从属知识点节点，颜色为绿色
        G.add_edge(title_id, skp)  # 添加边，表示题目到从属知识点的关系

        for kp in knowledge_points:
            G.add_node(kp, color='blue', title='知识点')  # 添加知识点节点，颜色为蓝色
            G.add_edge(skp, kp)  # 添加边，表示从属知识点到知识点的关系

# 创建Pyvis网络图#222222
net = Network(notebook=True, height="750px", width="100%", bgcolor="white", font_color="#222222")

# 将networkx图添加到Pyvis图
net.from_nx(G)

# 设置节点物理属性（可选）
net.show_buttons(filter_=['physics'])

# 显示网络图
net.show("knowledge_network.html")

