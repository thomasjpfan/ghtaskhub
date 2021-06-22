import sys

from github import Github

from ._utils import _get_info


def delete(github_token, taskhub_repo, project_repo, project_number):
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
    for column in columns:
        cards = column.get_cards()
        for card in cards:
            _, _, card_number, _ = _get_info(card.note)
            if int(card_number) == int(project_number):
                card.delete()
                print(f"Deleting Issue/PR #{project_number} from {column.name}")
                sys.exit(0)

    print(f"Unable to find Issue/PR #{project_number}")
    sys.exit(1)
