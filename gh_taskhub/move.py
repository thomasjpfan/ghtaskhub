import sys
from ghapi.all import GhApi

from ._utils import _get_info


def move(
    github_token, taskhub_repo, project_repo, project_number, from_column, to_column
):
    owner, repo = taskhub_repo.split("/")

    taskhub_api = GhApi(owner=owner, repo=repo, token=github_token)

    projects = taskhub_api.projects.list_for_repo()

    for project in projects:
        if project.name != project_repo:
            continue

        columns = taskhub_api.projects.list_columns(project.id)
        from_id = None
        to_id = None
        for column in columns:
            if column.name == from_column:
                from_id = column.id
            elif column.name == to_column:
                to_id = column.id

        if from_id is None:
            print(f"There is not a {from_column} column in {project.name}")
            sys.exit(1)

        if to_id is None:
            print(f"There are not a {to_column} column in {project.name}")
            sys.exit(1)

        from_cards = taskhub_api.projects.list_cards(from_id)
        for card in from_cards:
            _, _, number = _get_info(card.note)
            if int(number) == project_number:
                taskhub_api.projects.move_card(card.id, "top", to_id)
                print(f"Moved issue {project_number} to be actionable")
                break
        else:  # no break
            print(f"Issue {project_number} was not found")
