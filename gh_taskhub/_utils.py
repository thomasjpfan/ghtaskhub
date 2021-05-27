import re


def _get_info(note):
    regex_str = r"https://github\.com/([\w-]+)/([\w-]+)/(issues|pull)/(\d+)"
    url_re = re.compile(regex_str)

    results = url_re.search(note)
    owner, repo, _, number = results.groups()
    return owner, repo, number, len(note)
