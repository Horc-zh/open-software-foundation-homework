import os
from time import sleep

import github

token = os.getenv("GITHUB_TOKEN")
repo_url = "simplejson/simplejson"

gh = github.Github(token)
repo = gh.get_repo("simplejson/simplejson")


for issue in repo.get_issues(state="all"):
    comment = issue.get_comments()
    issue_create_at = issue.created_at
    issue_id = issue.id
    print(issue.id, issue.created_at, end="\t")
    if comment.totalCount > 0:
        first_comment_create_at = comment[0].created_at
        print(comment[0].created_at)
        print(comment[0].created_at - issue.created_at)
    else:
        print("no comment")

    sleep(0.2)
