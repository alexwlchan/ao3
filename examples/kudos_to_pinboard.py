#!/usr/bin/env python
# -*- encoding: utf-8
"""
A script for syncing kudos from AO3 to Pinboard.

You need the ``ao3`` module installed to use this script.  Original idea from
https://twitter.com/anatsuno/status/427177496875122688

To use this script:

1.  Enable Viewing History on AO3
    (My Preferences > Preferences > Misc > Turn on Viewing History)

2.  Fill in your AO3 and Pinboard credentials below.

3.  Run the script: ``python kudos_to_pinboard.py``.  Any items on AO3 that
    you've read in the last seven days, and where you've left kudos, will
    be added to Pinboard if you don't already have a bookmark.

    The new bookmarks are tagged `ao3_kudos_sync`.

"""

from datetime import datetime, timedelta

from ao3 import AO3
from ao3.works import RestrictedWork
import requests


# AO3 login credentials
AO3_USERNAME = '<USERNAME>'
AO3_PASSWORD = '<PASSWORD>'

# Pinboard API token.  https://pinboard.in/settings/password
PINBOARD_API_TOKEN = '<API_TOKEN>'


def main():
    api = AO3()
    api.login(username=AO3_USERNAME, password=AO3_PASSWORD)

    for work_id, last_read in api.user.reading_history():
        if last_read < (datetime.now() - timedelta(days=7)).date():
            break
        try:
            work = api.work(id=work_id)
        except RestrictedWork:
            print('Skipping %s as a restricted work' % work_id)
            continue
        if api.user.username in work.kudos_left_by:
            title = '%s - %s - %s [Archive of Our Own]' % (
                work.title, work.author, work.fandoms[0])
            print('Saving %s to Pinboard...' % work.url)
            requests.get('https://api.pinboard.in/v1/posts/add', params={
                'url': work.url,
                'description': title,
                'tags': 'ao3_kudos_sync',
                'replace': 'no',
                'auth_token': PINBOARD_API_TOKEN,
                'format': 'json',
            })


if __name__ == '__main__':
    main()
