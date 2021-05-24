import sys
from github import Github
import os
import argparse

bucket_name = "Bucket List"

parser = argparse.ArgumentParser(description="Add bucket")
parser.add_argument("repo", type=str)
parser.add_argument("number", type=int)
args = parser.parse_args()

token = os.getenv("GITHUB_TOKEN")
repo_name = os.getenv("GITHUB_REPOSITORY", "thomasjpfan/taskhub")

g = Github(token)
repo = g.get_repo(repo_name)

projects = repo.get_projects()

target_project = None
for project in projects:
    if project.name == args.repo:
        target_project = project
        break
else:  # no break
    print(f"Can not find {args.repo}")
    sys.exit(1)


columns = target_project.get_columns()
target_column = None
for column in columns:
    if column.name == bucket_name:
        target_column = column
        break
else:  # no break
    print(f"Can not find column: {bucket_name}")
    sys.exit(1)

note = f"https://github.com/{args.repo}/issues/{args.number}"
target_column.create_card(note=note)
print(f"Added {note} to column: {bucket_name}")
