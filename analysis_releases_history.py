import requests
import pandas as pd
import matplotlib.pyplot as plt
import re

def fetch_releases(owner, repo):
    """
    从 GitHub API 获取指定仓库的 Releases 数据
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/releases"
    print(f"正在从 GitHub API 获取 {owner}/{repo} 的 Releases 数据...")
    try:
        response = requests.get(url)
        response.raise_for_status()
        releases = response.json()
        print(f"成功获取 Releases 数据！\n总计 {len(releases)} 条 Release 记录。")
        return releases
    except requests.RequestException as e:
        print(f"获取 Releases 数据失败：{e}")
        return []

def analyze_release_content(releases):
    data = []
    for release in releases:
        release_name = release.get("name", "Unknown")
        published_at = release.get("published_at", "Unknown")
        author = release.get("author", {}).get("login", "Unknown")
        body = release.get("body", "") or ""  # 确保 body 不为 None

        # 行为分类
        feature_count = len(re.findall(r'\b(feature|add|new|enhance|implement)\b', body, re.IGNORECASE))
        bug_fix_count = len(re.findall(r'\b(fix|bug|error|patch|hotfix)\b', body, re.IGNORECASE))
        doc_update_count = len(re.findall(r'\b(doc|documentation|readme|manual)\b', body, re.IGNORECASE))
        performance_count = len(re.findall(r'\b(optimize|refactor|improve|performance)\b', body, re.IGNORECASE))
        other_count = len(body.split('\n')) - (feature_count + bug_fix_count + doc_update_count + performance_count)

        data.append({
            "release_name": release_name,
            "published_at": published_at,
            "author": author,
            "features": feature_count,
            "bug_fixes": bug_fix_count,
            "doc_updates": doc_update_count,
            "performance": performance_count,
            "other": other_count
        })
    return pd.DataFrame(data)


def plot_release_frequency(df):
    """
    绘制发布频率折线图
    """
    df['published_at'] = pd.to_datetime(df['published_at'])
    release_counts = df['published_at'].dt.date.value_counts().sort_index()

    plt.figure(figsize=(12, 6))
    release_counts.plot(kind='line', marker='o')
    plt.title("Release Frequency Over Time")
    plt.xlabel("Date")
    plt.ylabel("Number of Releases")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("release_frequency.png")
    plt.show()

def plot_behavior_distribution(df):
    """
    绘制各类行为分布柱状图
    """
    behavior_summary = df[['features', 'bug_fixes', 'doc_updates', 'performance', 'other']].sum()

    plt.figure(figsize=(10, 6))
    behavior_summary.plot(kind='bar', color='skyblue')
    plt.title("Distribution of Release Behaviors")
    plt.xlabel("Behavior Type")
    plt.ylabel("Total Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("behavior_distribution.png")
    plt.show()

def plot_behavior_trend(df):
    """
    绘制各类行为的时间趋势图
    """
    df['published_at'] = pd.to_datetime(df['published_at'])
    df = df.sort_values('published_at')

    behavior_trends = df.set_index('published_at')[['features', 'bug_fixes', 'doc_updates', 'performance', 'other']].resample('M').sum()

    plt.figure(figsize=(12, 6))
    for column in behavior_trends.columns:
        plt.plot(behavior_trends.index, behavior_trends[column], label=column.capitalize())

    plt.title("Behavior Trends Over Time")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.legend()
    plt.tight_layout()
    plt.savefig("behavior_trends.png")
    plt.show()

def save_analysis_results(df):
    """
    保存分析结果到文件
    """
    print("\n保存分析结果到文件...")
    df.to_csv("release_analysis.csv", index=False)
    print("结果已保存到 'release_analysis.csv'")

def main():
    owner = "simplejson"
    repo = "simplejson"

    # 获取 Releases 数据
    releases = fetch_releases(owner, repo)
    if not releases:
        print("未获取到 Releases 数据，程序退出。")
        return

    # 分析 Releases 内容
    df = analyze_release_content(releases)

    # 绘制图表
    plot_release_frequency(df)
    plot_behavior_distribution(df)
    plot_behavior_trend(df)

    # 保存结果
    save_analysis_results(df)

if __name__ == "__main__":
    main()
