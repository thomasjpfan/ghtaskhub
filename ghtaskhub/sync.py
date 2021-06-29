import sys
from collections import defaultdict
import re
import datetime

from ghapi.all import GhApi

from ._utils import _get_info
from .columns import Column
from .move import _move_card


def sync(github_token, taskhub_repo, project_repo):

    owner, repo = taskhub_repo.split("/")
    taskhub_api = GhApi(owner=owner, repo=repo, token=github_token)

    projects = taskhub_api.projects.list_for_repo()

    repo_apis = {}

    def _get_repo_api(owner, repo):
        if (owner, repo) in repo_apis:
            api = repo_apis[owner, repo]
        else:
            api = GhApi(owner=owner, repo=repo, token=github_token)
            repo_apis[owner, repo] = api
        return api

    def _is_open(owner, repo, number):
        api = _get_repo_api(owner, repo)
        return api.issues.get(number).state == "open"

    number_to_card_ids = defaultdict(list)

    if project_repo == "all":
        projects_to_sync = projects
    else:
        projects_to_sync = [
            project for project in projects if project.name == project_repo
        ]

    if not projects_to_sync:
        print(f"{project_repo} was not found in projects")
        sys.exit(1)

    for project in projects_to_sync:
        print(f"Syncing {project.name}")
        columns = taskhub_api.projects.list_columns(project.id)

        column_name_to_enum = {v.value: v for k, v in Column.__members__.items()}
        column_enum_to_ids = {
            column_name_to_enum[column.name]: column.id for column in columns
        }
        other_ids = [
            col_id for enum, col_id in column_enum_to_ids if enum != Column.DONE
        ]

        # move cards to done if they were closed.
        for col_id in other_ids:
            cards = taskhub_api.projects.list_cards(col_id)
            for card in cards:
                owner, repo, number, note_size = _get_info(card.note)
                number_to_card_ids[number].append((note_size, card.id))

                if not _is_open(owner, repo, number):
                    _move_card(taskhub_api, card, column_enum_to_ids[Column.DONE])
                elif column_enum_to_ids[Column.WAITING_FOR_RESPONSE] == col_id:
                    repo_api = _get_repo_api(owner, repo)
                    _move_waiting(
                        taskhub_api, repo_api, card, column_enum_to_ids, number, owner
                    )

    for number, id_infos in number_to_card_ids.items():
        if len(id_infos) <= 1:
            continue

        print(f"Removing cards for {number} because of duplicates")
        sorted_info = sorted(id_infos)
        for _, card_id in sorted_info[:-1]:
            taskhub_api.projects.delete_card(card_id)


def _move_waiting(taskhub_api, repo_api, card, column_enum_to_ids, number, owner):
    card_date_match = re.search("Added: (.+)", card.note)
    if card_date_match is None:
        return

    card_date_str = card_date_match.group(1)
    try:
        card_added_dt = datetime.datetime.fromisoformat(card_date_str)
    except ValueError:
        return

    info = repo_api.issues.get(number)
    if not hasattr(info, "pul_request"):
        return

    pr = repo_api.pulls.get(number)

    if pr.user == owner:
        # MY PR & Review by someone else -> Move to "Actionable"
        _ = repo_api.pulls.list_reviews(number, per_page=1)
        last_page = repo_api.last_page()
        last_review = repo_api.pulls.list_reviews(number, per_page=1, page=last_page)
        if last_review.user.login == owner:
            return

        try:
            review_dt = datetime.datetime.fromisoformat(
                last_review.replace("Z", "+00:00")
            )
        except ValueError:
            return

        if review_dt > card_added_dt:
            _move_card(taskhub_api, card, column_enum_to_ids[Column.ACTIONABLE])
    else:
        # Not my PR & updated by contributor -> Move to "To Review"
        updated_at = pr.head.repo.updated_at

        try:
            updated_dt = datetime.datetime.fromisoformat(
                updated_at.replace("Z", "+00:00")
            )
        except ValueError:
            return

        if updated_dt > card_added_dt:
            _move_card(taskhub_api, card, column_enum_to_ids[Column.TO_REVIEW])
