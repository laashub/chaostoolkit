# -*- coding: utf-8 -*-
import re

from logzero import logger
import requests

from chaostoolkit import __version__

__all__ = ["check_newer_version"]

LATEST_RELEASE_URL = "https://releases.chaostoolkit.org/latest"
CHANGELOG_URL = "https://github.com/chaostoolkit/chaostoolkit/blob/master/CHANGELOG.md"  # nopep8


def check_newer_version():
    """
    Query for the latest release of the chaostoolkit to compare it
    with the current's version. If the former is higher then issue a warning
    inviting the user to upgrade its environment.
    """
    try:
        r = requests.get(LATEST_RELEASE_URL, timeout=(1, 30),
                         params={"current": __version__})
        if r.status_code == 200:
            payload = r.json()
            latest_version = payload["version"]
            if payload.get("up_to_date") is False:
                logger.warn(
                    "\nThere is a new version ({v}) of the chaostoolkit "
                    "available.\n"
                    "You may upgrade by typing:\n\n"
                    "$ pip install -U chaostoolkit\n\n"
                    "Please review changes at {u}\n".format(
                        u=CHANGELOG_URL, v=latest_version))
                return latest_version
    except Exception:
        raise
