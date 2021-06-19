import sys
from ghapi.all import GhApi

from ._utils import _get_info


def move(github_token, taskhub_repo, project_repo, project_number, to_column):
    owner, repo = taskhub_repo.split("/")

    taskhub_api = GhApi(owner=owner, repo=repo, token=github_token)

    projects = taskhub_api.projects.list_for_repo()

    for project in projects:
        if project.name != project_repo:
            continue

        columns = taskhub_api.projects.list_columns(project.id)
        to_id = None
        other_columns = []
        for column in columns:
            if column.name == to_column:
                to_id = column.id
            elif column.name != "Done":
                other_columns.append(column)

        if to_id is None:
            print(f"There are not a {to_column} column in {project.name}")
            sys.exit(1)

        moved = False
        for column in other_columns:
            if moved:
                break

            from_id = column.id
            from_column = column.name
            from_cards = taskhub_api.projects.list_cards(from_id)
            for card in from_cards:
                _, _, number = _get_info(card.note)
                if int(number) != project_number:
                    taskhub_api.projects.move_card(card.id, "top", to_id)
                    print(
                        f"Moved issue {project_number} from {from_column} to"
                        f" {to_column}"
                    )
                    moved = True
                    break

        if not moved:
            print(
                f"{project_number} was not found, please add it to the bucket list"
                " first"
            )
