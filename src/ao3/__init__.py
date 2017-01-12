# -*- encoding: utf-8

from .works import Work


class AO3(object):
    """A scraper for the Archive of Our Own (AO3)."""

    def __repr__(self):
        return '%s()' % (type(self).__name__)

    def work(self, id):
        """Look up a work that's been posted to AO3.

        :param id: the work ID.  In the URL to a work, this is the number.
            e.g. the work ID of http://archiveofourown.org/works/1234 is 1234.
        """
        return Work(id=id)
