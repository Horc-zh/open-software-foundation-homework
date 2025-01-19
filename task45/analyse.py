import pandas as pd
import matplotlib.pyplot as plt
import re

from statsmodels.tsa.arima.model import ARIMA


#非常坏csv ,使我读取失败。（列内容里面带有逗号，还不加引号！）
data = pd.read_csv(r'data/commit_history.csv', names=['commit_hash', 'author', 'time', 'version'],index_col=False,on_bad_lines='skip')
print(data.head())
print(len(data.columns))
data['time'] = pd.to_datetime(data['time'])


# 统计每一天的提交数量，作为热力值
daily_commits = data.groupby('time').size()

# 存版本信息的日期
version_dates = []

# 查找“类似 v ****”的版本信息，并记录版本号和对应的日期
for index, row in data.iterrows():
    version = str(row['version'])
    if re.match(r'v\s*\d+\.\d+\.\d+', version):
        version_dates.append((version, row['time']))


authors = data['author'].unique()
author_commits = {}
# 按作者分组并统计每一天的提交数量
for author in authors:
    author_data = data[data['author'] == author]
    author_daily_commits = author_data.groupby('time').size()
    author_commits[author] = author_daily_commits

# 绘制热力图（提交量）
plt.figure(figsize=(10, 6))
plt.plot(daily_commits.index, daily_commits.values, label='Commit Heat', color='blue')


# 为每个版本点添加竖线标记
for version, version_date in version_dates:
    version_date = pd.to_datetime(version_date)
    plt.axvline(x=version_date, color='red', linestyle='--', label=version)

plt.title('Commit Heat over Time with Version Updates')
plt.xlabel('Date')
plt.ylabel('Commit Heat')

# 避免重复的竖线标签
handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(12, 8))
# 为每个作者的提交热力图绘制折线
for author, commits in author_commits.items():
    if author != 'Bob Ippolito':
        plt.plot(commits.index, commits.values, linewidth=2, label='Other Authors')
        plt.scatter(commits.index, commits.values, color='red', zorder=5,alpha=0.7,s=20, edgecolors='red') 
for author, commits in author_commits.items():
    if author == 'Bob Ippolito':
        plt.scatter(commits.index, commits.values, color='blue', zorder=4,alpha=0.4,s=20, label='Bob Ippolito', facecolors='none', edgecolors='blue') 
plt.title('Individual Author Commit Heat over Time')
plt.xlabel('Date')
plt.ylabel('Commit Heat')


handles, labels = plt.gca().get_legend_handles_labels()
by_label = dict(zip(labels, handles))
plt.legend(by_label.values(), by_label.keys())

plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig('individual_author_commit_heat.png')  # 可选：保存图片
plt.show()  

daily_commits = daily_commits.resample('D').sum()
# 拟合 ARIMA 模型 
model = ARIMA(daily_commits, order=(1, 1,10 ))
model_fit = model.fit()

# 预测未来一年（365天）
forecast = model_fit.forecast(steps=365)
print(forecast)
# 创建预测的日期范围
forecast_dates = pd.date_range(start=daily_commits.index[-1] + pd.Timedelta(days=1), periods=365, freq='D')

# 绘制实际提交量和预测的提交量
plt.figure(figsize=(10, 6))
plt.plot(daily_commits.index, daily_commits.values, label='Actual Commits')
plt.plot(forecast_dates, forecast, label='Forecasted Commits', color='red')
plt.title('Commit Forecast for the Next Year')
plt.xlabel('Date')
plt.ylabel('Number of Commits')
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
#plt.savefig('Commit Forecast for the Next Year.png')