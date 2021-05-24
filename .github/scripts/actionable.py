import sys
import re
from collections import defaultdict
import argparse
import os

repo_name = os.getenv("GITHUB_REPOSITORY", "thomasjpfan/taskhub")

from ghapi.all import GhApi  # noqa
from ghapi.all import github_token  # noqa


owner, repo = repo_name.split("/")
waiting_name = "Waiting for Response"
actionable_name = "Actionable"


parser = argparse.ArgumentParser(description="Make actionable")
parser.add_argument("repo", type=str)
parser.add_argument("number", type=int)

args = parser.parse_args()

taskhub_api = GhApi(owner=owner, repo=repo, token=github_token())

projects = taskhub_api.projects.list_for_repo()

regex_number = r"https://github\.com/([\w-]+)/([\w-]+)/(issues|pull)/(\d+)"
number_re = re.compile(regex_number)

regex_repo = r"https://github\.com/([\w-]+)/([\w-]+)"
repo_re = re.compile(regex_repo)


def _get_info(card):
    note = card.note
    results = number_re.search(note)
    owner, repo, _, number = results.groups()
    return owner, repo, number


number_to_card_ids = defaultdict(list)
for project in projects:
    if project.name != args.repo:
        continue

    columns = taskhub_api.projects.list_columns(project.id)
    action_id = None
    waiting_id = None
    for column in columns:
        if column.name == actionable_name:
            action_id = column.id
        elif column.name == waiting_name:
            waiting_id = column.id

    if action_id is None:
        print(f"There is not a actionable column in {project.name}")
        sys.exit(1)

    if waiting_id is None:
        print(f"There are not a waiting columns in {project.name}")
        sys.exit(1)

    waiting_cards = taskhub_api.projects.list_cards(waiting_id)
    for card in waiting_cards:
        _, _, number = _get_info(card)
        if int(number) == args.number:
            taskhub_api.projects.move_card(card.id, "top", action_id)
            print(f"Moving issue {number} to be actionable")
            break
