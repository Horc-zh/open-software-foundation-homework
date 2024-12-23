import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# 读取CSV文件
df = pd.read_csv(
    "issue_info.csv",
    parse_dates=["issue_create_at", "first_comment_create_at", "reply_time"],
)
print(df["reply_time"])

# 分析没有回复的 issue
# 过滤掉那些没有回复的记录
no_reply_df = df[df["first_comment_create_at"] == "no comment"]
print(f"没有回复的issue数量: {no_reply_df.shape[0]}")

# 按每年分析 issue 发布的时间分布
# 提取 issue 发布的年份
df["issue_create_year"] = df["issue_create_at"].dt.to_period("Y")

# 绘制 issue 发布的年份分布
plt.figure(figsize=(14, 8))
sns.countplot(
    x="issue_create_year",
    data=df,
    palette="viridis",
    order=df["issue_create_year"].value_counts().index,
)
plt.title("Issue 发布的年度分布")
plt.xlabel("年份")
plt.ylabel("发布的Issue数量")
plt.xticks(rotation=45)
plt.show()
