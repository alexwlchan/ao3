# -*- encoding: utf-8
"""Utility functions."""

import re

# Regex for extracting the work ID from an AO3 URL.  Designed to match URLs
# of the form
#
#     https://archiveofourown.org/works/1234567
#     http://archiveofourown.org/works/1234567
#
WORK_URL_REGEX = re.compile(
    r'^https?://archiveofourown.org/works/'
    r'(?P<work_id>[0-9]+)'
)


def work_id_from_url(url):
    """Given an AO3 URL, return the work ID."""
    match = WORK_URL_REGEX.match(url)
    if match:
        return match.group('work_id')
    else:
        raise RuntimeError('%r is not a recognised AO3 work URL')
