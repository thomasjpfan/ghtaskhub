import sys
from os import environ
import re

from ghapi.all import GhApi

repo_name = "thomasjpfan/taskhub"
done_name = "Done"

repo_split = repo_name.split("/")
if len(repo_split) != 2:
    print("Repository name must be of the format OWNER/REPO")
owner, repo = repo_split

token = environ["GPPR_GITHUB_API_TOKEN"]
taskhub_api = GhApi(owner=owner, repo=repo, token=token)

projects = taskhub_api.projects.list_for_repo()

repo_apis = {}


regex_str = r"https://github\.com/(\w+)/(\w+)/(issues|pull)/(\d+)"
url_re = re.compile(regex_str)

repo_apis = {}


def _is_closed(note):
    results = url_re.search(note)
    owner, repo, _, number = results.groups()

    if (owner, repo) in repo_apis:
        api = repo_apis[owner, repo]
    else:
        api = GhApi(owner=owner, repo=repo, token=token)
        repo_apis[owner, repo] = api
    return api.issues.get(number).state == "closed"


for project in projects:
    columns = taskhub_api.projects.list_columns(project.id)
    done_id = None
    other_ids = []
    for column in columns:
        if column.name == done_name:
            done_id = column.id
        else:
            other_ids.append(column.id)

    if done_id is None:
        print(f"There is not done column in {project.name}")
        sys.exit(1)

    if not other_ids:
        print(f"There are no other columns in {project.name}")
        sys.exit(1)

    # Check cards if it is "done"
    for col_id in other_ids:
        cards = taskhub_api.projects.list_cards(col_id)
        for card in cards:
            if not _is_closed(cards):
                continue
            taskhub_api.projects.move_card(card.id, "top", done_id)
