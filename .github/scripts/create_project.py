import argparse
import os

repo_name = os.getenv("GITHUB_REPOSITORY", "thomasjpfan/taskhub")

from ghapi.all import GhApi  # noqa
from ghapi.all import github_token  # noqa

owner, repo = repo_name.split("/")

parser = argparse.ArgumentParser(description="Create project")
parser.add_argument("repo", type=str)

args = parser.parse_args()

taskhub_api = GhApi(owner=owner, repo=repo, token=github_token())

body = f"https://github.com/{args.repo}"
project = taskhub_api.projects.create_for_repo(args.repo, body)
print(f"Added project: {project}")

columns = ["Bucket List", "Actionable", "Waiting for Response", "Done"]
for column in columns:
    taskhub_api.projects.create_column(project.id, column)
    print(f"Added column: {column}")
