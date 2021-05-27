import sys

from github import Github

from ._utils import _get_info


def add_bucket(github_token, taskhub_repo, project_repo, project_number):
    bucket_name = "Bucket List"

    g = Github(github_token)
    repo = g.get_repo(taskhub_repo)

    projects = repo.get_projects()

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
        if column.name == bucket_name:
            target_column = column
            break
    else:  # no break
        print(f"Can not find column: {bucket_name}")
        sys.exit(1)

    cards = target_column.get_cards()
    for card in cards:
        _, _, card_number, _ = _get_info(card.note)
        if card_number == project_number:
            break
    else:  # no break
        print(f"Issue/PR #{project_number} is already in {bucket_name}")
        sys.exit(0)

    note = f"https://github.com/{project_repo}/issues/{project_number}"
    target_column.create_card(note=note)
    print(f"Added {note} to column: {bucket_name}")
