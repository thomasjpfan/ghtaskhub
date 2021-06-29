import sys
from ghapi.all import GhApi

from ._utils import _get_info
from .add import add
from .add import _add_date_to_note
from .columns import Column


def move(github_token, taskhub_repo, project_repo, project_number, to_column_enum):
    owner, repo = taskhub_repo.split("/")

    taskhub_api = GhApi(owner=owner, repo=repo, token=github_token)

    projects = taskhub_api.projects.list_for_repo()
    to_column = to_column_enum.value

    for project in projects:
        if project.name != project_repo:
            continue

        columns = taskhub_api.projects.list_columns(project.id)
        to_id = None
        other_columns = []
        for column in columns:
            if column.name == to_column:
                to_id = column.id
            elif column.name != Column.DONE.value:
                other_columns.append(column)

        if to_id is None:
            print(f"There are not a {to_column} column in {project.name}")
            sys.exit(1)

        for column in other_columns:
            from_id = column.id
            from_column = column.name
            from_cards = taskhub_api.projects.list_cards(from_id)
            for card in from_cards:
                _, _, number, _ = _get_info(card.note)
                if int(number) == project_number:
                    _move_card(taskhub_api, card.id, to_id)
                    print(
                        f"Moved issue {project_number} from {from_column} to"
                        f" {to_column}"
                    )
                    return

        other_names = ", ".join([column.name for column in other_columns])
        print(f"{project_number} was not found in [{other_names}]")
        print(f"Creating {project_number} and adding it to {to_column}")
        add(github_token, taskhub_repo, project_repo, project_number, to_column_enum)


def _move_card(taskhub_api, card, to_id):
    taskhub_api.projects.move_card(card.id, "top", to_id)
    new_note = _add_date_to_note(card.note)
    taskhub_api.projects.update_card(card.id, new_note)
