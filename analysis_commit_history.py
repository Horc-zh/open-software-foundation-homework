import os
import pandas as pd
import matplotlib.pyplot as plt

def load_commit_history(file_path):
    """
    加载提交历史数据
    :param file_path: CSV 文件路径
    :return: pandas DataFrame
    """
    print("读取 commit_history.csv 文件...")
    try:
        df = pd.read_csv(file_path, names=["hash", "author", "date", "message"], comment='#', on_bad_lines='skip')
        print("数据加载成功！")
        print("\n提交历史数据（前5行）：")
        print(df.head())
        return df
    except Exception as e:
        print(f"加载文件时发生错误：{e}")
        return None

def analyze_commit_by_author(df):
    """
    按作者统计提交次数
    """
    print("\n统计每个作者的提交次数...")
    commit_counts = df['author'].value_counts()
    print(commit_counts)
    return commit_counts

def analyze_commit_frequency(df):
    """
    按日期统计提交数量，并绘制折线图
    """
    print("\n分析提交频率（按日期）...")
    # 将日期转换为标准 datetime 格式
    df['date'] = pd.to_datetime(df['date'], errors='coerce')
    daily_commits = df['date'].dt.date.value_counts().sort_index()

    print("提交频率（按日期）：")
    print(daily_commits)

    # 绘制折线图
    plt.figure(figsize=(10, 6))
    daily_commits.plot(kind='line', marker='o', linestyle='-')
    plt.title("Commit Frequency Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Commits")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("commit_frequency.png")  # 保存图像
    plt.show()

def analyze_version_releases(df):
    """
    统计版本发布的次数 (message 包含 'v3.' 作为版本号标识)
    """
    print("\n统计版本发布次数...")
    version_commits = df[df['message'].str.contains(r'v3\.\d+\.\d+', na=False)]
    print(f"找到 {len(version_commits)} 条版本发布记录：")
    print(version_commits[['date', 'message']])
    return version_commits

def save_results(commit_counts, version_commits):
    """
    保存统计结果到文件
    """
    print("\n保存分析结果到文件...")
    commit_counts.to_csv("commit_counts_by_author.csv", header=True)
    version_commits.to_csv("version_releases.csv", index=False)
    print("结果已保存到 'commit_counts_by_author.csv' 和 'version_releases.csv'")

def main():
    # 定义文件路径
    file_path = "commit_history.csv"
    
    # 加载数据
    df = load_commit_history(file_path)
    if df is None:
        print("无法加载数据，程序退出。")
        return
    
    # 分析提交者统计
    commit_counts = analyze_commit_by_author(df)
    
    # 提交频率分析
    analyze_commit_frequency(df)
    
    # 版本发布统计
    version_commits = analyze_version_releases(df)
    
    # 保存结果
    save_results(commit_counts, version_commits)

if __name__ == "__main__":
    main()
