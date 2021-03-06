from functools import partial
import os
import argparse
import sys

from .move import move
from .create_project import create_project
from .sync import sync
from .columns import Column
from .delete import delete


def main():
    parser = argparse.ArgumentParser(description="Control your taskhub")
    parser.add_argument(
        "project_repo",
        type=str,
    )
    parser.add_argument(
        "--github-token",
        default=os.getenv("GITHUB_TOKEN", None),
        help="github personal token",
    )
    parser.add_argument(
        "--taskhub-repo",
        default=os.getenv("TASKHUB_REPO", None),
        help="Name of taskhub repo",
    )
    subparser = parser.add_subparsers()

    move_columns = [
        ("bucket", "Move or add to bucket", Column.BUCKET),
        ("actionable", "Move or add to actionable", Column.ACTIONABLE),
        (
            "response",
            "Move or add to waiting for response",
            Column.WAITING_FOR_RESPONSE,
        ),
        ("to_review", "Move or add to review", Column.TO_REVIEW),
    ]

    for option, help_str, to_column in move_columns:
        option_parser = subparser.add_parser(option, help=help_str)
        option_parser.add_argument("project_number", type=int, help="issue number")
        option_partial = partial(move, to_column_enum=to_column)
        option_parser.set_defaults(func=option_partial)

    create_project_parser = subparser.add_parser(
        "create-project",
        help="Create project template",
    )
    create_project_parser.set_defaults(func=create_project)

    sync_parser = subparser.add_parser(
        "sync",
        help=(
            "sync project board (remove duplicates and "
            "move closed issues to Done column"
        ),
    )
    sync_parser.set_defaults(func=sync)

    delete_card_parser = subparser.add_parser("delete", help="Delete card")
    delete_card_parser.add_argument(
        "project_number", type=int, help="issue number to delete"
    )
    delete_card_parser.set_defaults(func=delete)

    args = parser.parse_args()

    if args.github_token is None:
        print("GITHUB_TOKEN or --github-token must be set")
        sys.exit(1)

    if args.taskhub_repo is None:
        print("TASKHUB_REPO or --taskhub-repo must be set")
        sys.exit(1)

    dict_args = {key: value for key, value in vars(args).items() if key != "func"}
    args.func(**dict_args)
