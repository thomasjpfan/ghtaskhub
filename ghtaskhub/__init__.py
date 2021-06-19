from functools import partial
import os
import argparse
import sys

from .move import move
from .add_bucket import add_bucket
from .create_project import create_project
from .sync import sync


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

    actionable_parser = subparser.add_parser(
        "actionable",
        help="Waiting for response is now actionable",
    )
    actionable_parser.add_argument(
        "project_number",
        type=int,
        help="issue number to make actionable",
    )
    actionable_partial = partial(
        move,
        to_column="Actionable",
    )
    actionable_parser.set_defaults(func=actionable_partial)

    response_parser = subparser.add_parser(
        "response",
        help="Actionable is now needs response",
    )
    response_parser.add_argument(
        "project_number",
        type=int,
        help="issue number to waiting for response",
    )
    response_partial = partial(
        move,
        to_column="Waiting for Response",
    )
    response_parser.set_defaults(func=response_partial)

    bucket_parser = subparser.add_parser(
        "bucket",
        help="Add issue to bucket",
    )
    bucket_parser.add_argument(
        "project_number",
        type=int,
        help="issue number to make actionable",
    )
    bucket_parser.set_defaults(func=add_bucket)

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

    args = parser.parse_args()

    if args.github_token is None:
        print("GITHUB_TOKEN or --github_token must be set")
        sys.exit(1)

    if args.taskhub_repo is None:
        print("TASKHUB_REPO or --taskhub-repo must be set")
        sys.exit(1)

    dict_args = {key: value for key, value in vars(args).items() if key != "func"}
    args.func(**dict_args)
