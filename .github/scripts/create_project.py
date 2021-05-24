import argparse
from ghapi.all import GhApi
from ghapi.all import github_token

repo_name = "thomasjpfan/taskhub"
owner, repo = repo_name.split("/")

parser = argparse.ArgumentParser(description="Create project")
parser.add_argument("repo", type=str)

args = parser.parse_args()

taskhub_api = GhApi(owner=owner, repo=repo, token=github_token())

body = f"https://github.com/{args.repo}"
project = taskhub_api.projects.create_for_repo(args.repo, body)

columns = ["Bucket List", "Actionable", "Waiting for Response", "Done"]
for column in columns:
    taskhub_api.projects.create_column(project.id, column)
