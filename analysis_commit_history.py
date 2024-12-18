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

import re

import re

def classify_commit_type(message):
    """
    细化提交类型的分类规则
    :param message: 提交信息
    :return: 提交类型
    """
    message = str(message).lower()  # 确保消息是小写的

    # 版本发布检测
    if re.search(r'v\d+\.\d+\.\d+', message):  # 匹配版本号（如 v3.19.3）
        return 'Version Release'

    # 功能增加或改进
    elif 'feature' in message or 'add' in message or 'new' in message or 'implement' in message or 'enhance' in message:
        return 'Feature'  # 功能/新特性

    # Bug 修复
    elif 'fix' in message or 'bug' in message or 'patch' in message or 'error' in message or 'hotfix' in message:
        return 'Bug Fix'  # Bug 修复

    # 性能优化或重构
    elif 'performance' in message or 'optimize' in message or 'refactor' in message or 'improve' in message:
        return 'Performance/Refactor'  # 性能优化或重构

    # 文档更新
    elif 'doc' in message or 'documentation' in message or 'readme' in message or 'update docs' in message or 'docs' in message:
        return 'Documentation'  # 文档更新

    # 测试
    elif 'test' in message or 'tests' in message or 'unittest' in message or 'integration' in message:
        return 'Test'  # 测试

    # 配置或环境更新
    elif 'config' in message or 'environment' in message or 'docker' in message or 'ci' in message or 'ci/cd' in message:
        return 'Configuration/Environment'  # 配置/环境

    # 安全更新
    elif 'security' in message or 'vulnerability' in message or 'exploit' in message or 'fix security' in message:
        return 'Security'  # 安全更新

    # 其他类型（无法明确分类的）
    else:
        return 'Other'

def analyze_commit_types(df):
    """
    分析提交类型（如版本发布、功能增加、bug修复、性能优化、文档更新等）
    :param df: 提交历史数据的 DataFrame
    :return: 提交类型的统计信息
    """
    print("\n分析提交类型...")

    # 将每条提交的消息按规则分类
    df['type'] = df['message'].apply(classify_commit_type)

    # 统计每种类型的提交次数
    commit_types = df['type'].value_counts()

    print("提交类型分布：")
    print(commit_types)

    # 绘制提交类型的分布柱状图
    plt.figure(figsize=(10, 6))
    commit_types.plot(kind='bar', color='skyblue')
    plt.title("Commit Types Distribution")
    plt.xlabel("Commit Type")
    plt.ylabel("Number of Commits")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig("commit_types.png")  # 保存图像
    plt.show()

    # 返回提交类型统计信息
    return commit_types



def save_results(commit_counts, version_commits, commit_types):
    """
    保存统计结果到文件
    """
    print("\n保存分析结果到文件...")
    commit_counts.to_csv("commit_counts_by_author.csv", header=True)
    version_commits.to_csv("version_releases.csv", index=False)
    commit_types.to_csv("commit_types.csv", header=True)
    print("结果已保存到 'commit_counts_by_author.csv', 'version_releases.csv', 'commit_types.csv'")

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
    
    # 提交类型分析
    commit_types = analyze_commit_types(df)
    
    # 保存结果
    save_results(commit_counts, version_commits, commit_types)

if __name__ == "__main__":
    main()
