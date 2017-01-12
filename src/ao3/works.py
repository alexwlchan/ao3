# -*- encoding: utf-8

from bs4 import BeautifulSoup
import requests


class WorkNotFound(Exception):
    pass


class Work(object):

    def __init__(self, id):
        self.id = id

        # Fetch the HTML for this work
        sess = requests.Session()
        req = sess.get('https://archiveofourown.org/works/%s' % self.id)

        if req.status_code == 404:
            raise WorkNotFound('Unable to find a work with id %r' % self.id)
        elif req.status_code != 200:
            raise RuntimeError('Unexpected error from AO3 API: %r (%r)' %
                (req.text, req.statuscode))

        # For some works, AO3 throws up an interstitial page asking you to
        # confirm that you really want to see the adult works.  Yes, we do.
        if 'This work could have adult content' in req.text:
            req = sess.get(
                'https://archiveofourown.org/works/%s?view_adult=true' %
                self.id)

        self._html = req.text
        self._soup = BeautifulSoup(self._html, 'html.parser')

    def __repr__(self):
        return '%s(id=%r)' % (type(self).__name__, self.id)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return hash(repr(self))
