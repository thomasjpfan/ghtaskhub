from ghapi.all import GhApi  # noqa


def create_project(github_token, taskhub_repo, project_repo):
    owner, repo = taskhub_repo.split("/")

    taskhub_api = GhApi(owner=owner, repo=repo, token=github_token)

    body = f"https://github.com/{project_repo}"
    project = taskhub_api.projects.create_for_repo(project_repo, body)
    print(f"Added project: {project_repo}")

    columns = ["Bucket List", "Actionable", "Waiting for Response", "Done"]
    for column in columns:
        taskhub_api.projects.create_column(project.id, column)
        print(f"Added column: {column}")
