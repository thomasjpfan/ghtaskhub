import sys

from github import Github

from ._utils import _get_info


def add(github_token, taskhub_repo, project_repo, project_number, to_column_enum):
    g = Github(github_token)
    repo = g.get_repo(taskhub_repo)

    projects = repo.get_projects()

    to_column = to_column_enum.value
    target_project = None
    for project in projects:
        if project.name == project_repo:
            target_project = project
            break
    else:  # no break
        print(f"Can not find {project_repo}")
        sys.exit(1)

    columns = target_project.get_columns()
    target_column = None
    for column in columns:
        if column.name == to_column:
            target_column = column
            break
    else:  # no break
        print(f"Can not find column: {to_column}")
        sys.exit(1)

    cards = target_column.get_cards()
    for card in cards:
        _, _, card_number, _ = _get_info(card.note)
        if int(card_number) == int(project_number):
            print(f"Issue/PR #{project_number} is already in {to_column}")
            sys.exit(0)

    note = f"https://github.com/{project_repo}/issues/{project_number}"
    target_column.create_card(note=note)
    print(f"Added {note} to column: {to_column}")
