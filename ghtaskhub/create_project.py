from ghapi.all import GhApi  # noqa


def create_project(github_token, taskhub_repo, project_repo):
    owner, repo = taskhub_repo.split("/")

    taskhub_api = GhApi(owner=owner, repo=repo, token=github_token)

    body = f"https://github.com/{project_repo}"
    projects = taskhub_api.projects.list_for_repo()
    project_id = None
    for project in projects:
        if project.name == project_repo:
            project_id = project.id
            print(f"Project already created: {project_repo}")
            break
    else:  # no break
        project = taskhub_api.projects.create_for_repo(project_repo, body)
        project_id = project.id
        print(f"Added project: {project_repo}")

    columns = set(
        ["Bucket List", "Actionable", "Waiting for Response", "To Review", "Done"]
    )
    current_columns = set(
        col.name for col in taskhub_api.projects.list_columns(project_id)
    )
    missing_columns = columns - current_columns
    for column in missing_columns:
        taskhub_api.projects.create_column(project.id, column)
        print(f"Added column: {column}")
