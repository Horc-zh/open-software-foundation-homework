import csv
import os

import github

token = os.getenv("GITHUB_TOKEN")
repo_url = "simplejson/simplejson"

gh = github.Github(token)
repo = gh.get_repo("simplejson/simplejson")


with open("./issue_info.csv", mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        ["issue_id", "issue_create_at", "first_comment_create_at", "reply_time"]
    )

    for issue in repo.get_issues(state="all"):
        comment = issue.get_comments()
        issue_create_at = issue.created_at
        issue_id = issue.id
        if comment.totalCount > 0:
            first_comment_create_at = comment[0].created_at
            reply_time = first_comment_create_at - issue_create_at
            writer.writerow(
                [issue.number, issue_create_at, first_comment_create_at, reply_time]
            )
        else:
            writer.writerow([issue.number, issue_create_at, "no comment", "no comment"])

print("CSV file has been created successfully.")
