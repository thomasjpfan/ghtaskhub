import datetime
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

    url = f"https://github.com/{project_repo}/issues/{project_number}"
    target_column.create_card(note=_add_date_to_note(url))
    print(f"Added {project_repo}#{project_number} to column: {to_column}")


def _add_date_to_note(original_note):
    lines_split = original_note.split("\n")

    added_line = None
    for i, line in enumerate(lines_split):
        if line.startswith("Added: "):
            added_line = i
            break

    str_time = datetime.datetime.now(datetime.timezone.utc).isoformat()
    if added_line is None:
        return f"{original_note}\n\nAdded: {str_time}"

    lines_split[added_line] = f"Added: {str_time}"
    return "\n".join(lines_split)
