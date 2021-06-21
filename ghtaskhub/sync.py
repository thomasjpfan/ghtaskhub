import sys
from collections import defaultdict

from ghapi.all import GhApi

from ._utils import _get_info
from .columns import Column


def sync(github_token, taskhub_repo, project_repo):

    owner, repo = taskhub_repo.split("/")
    taskhub_api = GhApi(owner=owner, repo=repo, token=github_token)

    projects = taskhub_api.projects.list_for_repo()

    repo_apis = {}

    def _is_open(owner, repo, number):
        if (owner, repo) in repo_apis:
            api = repo_apis[owner, repo]
        else:
            api = GhApi(owner=owner, repo=repo, token=github_token)
            repo_apis[owner, repo] = api
        return api.issues.get(number).state == "open"

    number_to_card_ids = defaultdict(list)
    synced_something = False
    for project in projects:
        if not (project_repo == "all" or project_repo == project.name):
            continue
        synced_something = True
        print(f"Syncing {project.name}")
        columns = taskhub_api.projects.list_columns(project.id)
        done_id = None
        other_ids = []
        for column in columns:
            if column.name == Column.DONE.value:
                done_id = column.id
            else:
                other_ids.append(column.id)

        if done_id is None:
            print(f"There is not done column in {project.name}")
            sys.exit(1)

        if not other_ids:
            print(f"There are no other columns in {project.name}")
            sys.exit(1)

        for col_id in other_ids:
            cards = taskhub_api.projects.list_cards(col_id)
            for card in cards:
                owner, repo, number, note_size = _get_info(card.note)
                number_to_card_ids[number].append((note_size, card.id))

                if _is_open(owner, repo, number):
                    continue
                taskhub_api.projects.move_card(card.id, "top", done_id)

    for number, id_infos in number_to_card_ids.items():
        if len(id_infos) <= 1:
            continue

        print(f"Removing cards for {number} because of duplicates")
        sorted_info = sorted(id_infos)
        for _, card_id in sorted_info[:-1]:
            taskhub_api.projects.delete_card(card_id)

    if not synced_something:
        print(f"{project_repo} was not found in projects")
        sys.exit(1)
