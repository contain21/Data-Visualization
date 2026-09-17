import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
from catboost import CatBoostRegressor
import matplotlib.pyplot as plt
import numpy as np
'''
# 读取数据
student_summary = pd.read_csv('student_summary_new.csv')

# 删除不必要的列
columns_to_drop = ['total_knowledge_count', 'total_sub_knowledge_count']
student_summary = student_summary.drop(columns=columns_to_drop)

# 特征和目标变量
features = student_summary.drop(columns=['student_ID', 'total_score', 'any_correct_rate','correct_count'])
target_score = student_summary['total_score']
target_correct_rate = student_summary['any_correct_rate']

# 分割数据集为训练集和测试集
X_train, X_test, y_train_score, y_test_score = train_test_split(features, target_score, test_size=0.2, random_state=42)
X_train, X_test, y_train_correct, y_test_correct = train_test_split(features, target_correct_rate, test_size=0.2, random_state=42)

# 建立回归模型：可以尝试不同的模型
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest Regressor': RandomForestRegressor(n_estimators=100, random_state=42),
    'Gradient Boosting Regressor': GradientBoostingRegressor(n_estimators=100, random_state=42),
    'Support Vector Regressor': SVR(),
    'XGBoost Regressor': xgb.XGBRegressor(n_estimators=100, random_state=42),
    'CatBoost Regressor': CatBoostRegressor(iterations=100, depth=6, learning_rate=0.1, random_seed=42, verbose=0)
}

for model_name, model in models.items():
    # 预测 total_score
    model.fit(X_train, y_train_score)
    y_pred_score = model.predict(X_test)
    mse_score = mean_squared_error(y_test_score, y_pred_score)
    r2_score_val = r2_score(y_test_score, y_pred_score)
    print(f"{model_name} - Total Score: MSE = {mse_score}, R2 = {r2_score_val}")

    # 预测 any_correct_rate
    model.fit(X_train, y_train_correct)
    y_pred_correct = model.predict(X_test)
    mse_correct = mean_squared_error(y_test_correct, y_pred_correct)
    r2_correct = r2_score(y_test_correct, y_pred_correct)
    print(f"{model_name} - Correct Rate: MSE = {mse_correct}, R2 = {r2_correct}")

# 选择表现最好的模型进行进一步分析
best_model = RandomForestRegressor(n_estimators=100, random_state=42)
best_model.fit(X_train, y_train_score)
y_pred = best_model.predict(X_test)

# 特征重要性
importances = best_model.feature_importances_
feature_names = features.columns
indices = np.argsort(importances)

plt.figure(figsize=(12, 8))
plt.title('Feature Importances')
plt.barh(range(len(indices)), importances[indices], color='b', align='center')
plt.yticks(range(len(indices)), [feature_names[i] for i in indices])
plt.xlabel('Relative Importance')
plt.show()
'''
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score
import xgboost as xgb
from catboost import CatBoostRegressor
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.tree import plot_tree
from sklearn.inspection import PartialDependenceDisplay

# 读取数据
student_summary = pd.read_csv('student_summary_new.csv')

# 删除不必要的列
columns_to_drop = ['total_knowledge_count', 'total_sub_knowledge_count']
student_summary = student_summary.drop(columns=columns_to_drop)

# 特征和目标变量
features = student_summary.drop(columns=['student_ID', 'total_score', 'any_correct_rate'])
target_score = student_summary['total_score']
target_correct_rate = student_summary['any_correct_rate']

# 分割数据集为训练集和测试集
X_train, X_test, y_train_score, y_test_score = train_test_split(features, target_score, test_size=0.2, random_state=42)
X_train, X_test, y_train_correct, y_test_correct = train_test_split(features, target_correct_rate, test_size=0.2, random_state=42)

# 建立回归模型
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest Regressor': RandomForestRegressor(n_estimators=100, random_state=42),
    'Gradient Boosting Regressor': GradientBoostingRegressor(n_estimators=100, random_state=42),
    'XGBoost Regressor': xgb.XGBRegressor(n_estimators=100, random_state=42),
    'CatBoost Regressor': CatBoostRegressor(iterations=100, depth=6, learning_rate=0.1, random_seed=42, verbose=0)
}

results = {
    'Model': [],
    'MSE_Total_Score': [],
    'R2_Total_Score': [],
    'MSE_Correct_Rate': [],
    'R2_Correct_Rate': []
}

feature_importances = {}

for model_name, model in models.items():
    # 预测 total_score
    model.fit(X_train, y_train_score)
    y_pred_score = model.predict(X_test)
    mse_score = mean_squared_error(y_test_score, y_pred_score)
    r2_score_val = r2_score(y_test_score, y_pred_score)

    # 预测 any_correct_rate
    model.fit(X_train, y_train_correct)
    y_pred_correct = model.predict(X_test)
    mse_correct = mean_squared_error(y_test_correct, y_pred_correct)
    r2_correct = r2_score(y_test_correct, y_pred_correct)

    # 存储结果
    results['Model'].append(model_name)
    results['MSE_Total_Score'].append(mse_score)
    results['R2_Total_Score'].append(r2_score_val)
    results['MSE_Correct_Rate'].append(mse_correct)
    results['R2_Correct_Rate'].append(r2_correct)

    # 存储特征重要性
    if model_name == 'Linear Regression':
        feature_importances[model_name] = np.abs(model.coef_)
    else:
        feature_importances[model_name] = model.feature_importances_

# 转换结果为 DataFrame
results_df = pd.DataFrame(results)
results_df.to_csv('results_df.csv',index=False)
print(results_df)
# 可视化 MSE 和 R2
fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(14, 12))

# MSE 图表
axes[0].bar(results_df['Model'], results_df['MSE_Total_Score'], color='b', alpha=0.6, label='Total Score')
axes[0].bar(results_df['Model'], results_df['MSE_Correct_Rate'], color='r', alpha=0.6, label='Correct Rate')
axes[0].set_title('MSE Comparison')
axes[0].set_ylabel('Mean Squared Error')
axes[0].legend()

# R2 图表
axes[1].bar(results_df['Model'], results_df['R2_Total_Score'], color='b', alpha=0.6, label='Total Score')
axes[1].bar(results_df['Model'], results_df['R2_Correct_Rate'], color='r', alpha=0.6, label='Correct Rate')
axes[1].set_title('R2 Score Comparison')
axes[1].set_ylabel('R2 Score')
axes[1].legend()

plt.tight_layout()
plt.show()

# 可视化特征重要性
for model_name, importances in feature_importances.items():
    indices = np.argsort(importances)
    plt.figure(figsize=(12, 8))
    plt.title(f'Feature Importances - {model_name}')
    plt.barh(range(len(indices)), importances[indices], color='b', align='center')
    plt.yticks(range(len(indices)), [features.columns[i] for i in indices])
    plt.xlabel('Relative Importance')
    plt.show()

# 热力图显示所有模型的特征重要性
all_importances = pd.DataFrame({model_name: importances for model_name, importances in feature_importances.items()})
all_importances.index = features.columns

plt.figure(figsize=(14, 12))
sns.heatmap(all_importances, annot=True, cmap='coolwarm')
plt.title('Feature Importances Across Different Models')
plt.show()

# 绘制真实值和预测值之间的关系散点图
best_model_name = 'Random Forest Regressor'  # 选择表现最好的模型
best_model = models[best_model_name]
best_model.fit(X_train, y_train_score)
y_pred = best_model.predict(X_test)

plt.figure(figsize=(10, 6))
plt.scatter(y_test_score, y_pred, alpha=0.6)
plt.plot([y_test_score.min(), y_test_score.max()], [y_test_score.min(), y_test_score.max()], 'k--', lw=2)
plt.xlabel('True Values')
plt.ylabel('Predicted Values')
plt.title(f'True vs Predicted Values ({best_model_name})')
plt.show()

# 残差图
residuals = y_test_score - y_pred
plt.figure(figsize=(10, 6))
plt.scatter(y_pred, residuals, alpha=0.6)
plt.hlines(y=0, xmin=y_pred.min(), xmax=y_pred.max(), colors='r', linestyles='dashed')
plt.xlabel('Predicted Values')
plt.ylabel('Residuals')
plt.title(f'Residual Plot ({best_model_name})')
plt.show()

# 累积解释方差图（PCA）
from sklearn.decomposition import PCA

pca = PCA().fit(X_train)
plt.figure(figsize=(10, 6))
plt.plot(np.cumsum(pca.explained_variance_ratio_))
plt.xlabel('Number of Components')
plt.ylabel('Cumulative Explained Variance')
plt.title('PCA Cumulative Explained Variance')
plt.show()

# 决策树可视化（仅适用于随机森林）
if best_model_name == 'Random Forest Regressor':
    plt.figure(figsize=(20, 10))
    plot_tree(best_model.estimators_[0], feature_names=features.columns, filled=True, rounded=True)
    plt.show()

# 模型对比箱线图
plt.figure(figsize=(14, 8))
results_df_melted = results_df.melt(id_vars=['Model'], var_name='Metric', value_name='Value')
sns.boxplot(x='Metric', y='Value', hue='Model', data=results_df_melted)
plt.title('Model Performance Comparison')
plt.show()

# SHAP值
import shap

explainer = shap.Explainer(best_model, X_train)
shap_values = explainer(X_test)

plt.figure(figsize=(10, 6))
shap.summary_plot(shap_values, X_test)

