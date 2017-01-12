# -*- encoding: utf-8

from datetime import datetime
import json

from bs4 import BeautifulSoup, Tag
import requests


class WorkNotFound(Exception):
    pass


class RestrictedWork(Exception):
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
            raise RuntimeError('Unexpected error from AO3 API: %r (%r)' % (
                req.text, req.statuscode))

        # For some works, AO3 throws up an interstitial page asking you to
        # confirm that you really want to see the adult works.  Yes, we do.
        if 'This work could have adult content' in req.text:
            req = sess.get(
                'https://archiveofourown.org/works/%s?view_adult=true' %
                self.id)

        # Check for restricted works, which require you to be logged in
        # first.  See https://archiveofourown.org/admin_posts/138
        # To make this work, we'd need to have a common Session object
        # across all the API classes.  Not impossible, but fiddlier than I
        # care to implement right now.
        # TODO: Fix this.
        if 'This work is only available to registered users' in req.text:
            raise RestrictedWork('Looking at work ID %s requires login')

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

    @property
    def url(self):
        """A URL to this work."""
        return 'https://archiveofourown.org/works/%s' % self.id

    @property
    def title(self):
        """The title of this work."""
        # The title of the work is stored in an <h2> tag of the form
        #
        #     <h2 class="title heading">[title]</h2>
        #
        title_tag = self._soup.find('h2', attrs={'class': 'title'})
        return title_tag.contents[0].strip()

    @property
    def author(self):
        """The author of this work."""
        # The author of the work is kept in the byline, in the form
        #
        #     <h3 class="byline heading">
        #       <a href="/users/[author_name]" rel="author">[author_name]</a>
        #     </h3>
        #
        byline_tag = self._soup.find('h3', attrs={'class': 'byline'})
        a_tag = [t
                 for t in byline_tag.contents
                 if isinstance(t, Tag)]
        assert len(a_tag) == 1
        return a_tag[0].contents[0].strip()

    @property
    def summary(self):
        """The author summary of the work."""
        # The author summary is kept in the following format:
        #
        #     <div class="summary module" role="complementary">
        #       <h3 class="heading">Summary:</h3>
        #       <blockquote class="userstuff">
        #         [author_summary_html]
        #       </blockquote>
        #     </div>
        #
        summary_div = self._soup.find('div', attrs={'class': 'summary'})
        blockquote = summary_div.find('blockquote')
        return blockquote.renderContents().decode('utf8').strip()

    def _lookup_stat(self, class_name):
        """Returns the value of a stat."""
        # The stats are stored in a series of divs of the form
        #
        #     <dd class="[field_name]">[field_value]</div>
        #
        # This is a convenience method for looking up values from these divs.
        #
        dd_tag = self._soup.find('dd', attrs={'class': class_name})
        if 'tags' in dd_tag.attrs['class']:
            return self._lookup_list_stat(dd_tag=dd_tag)
        return dd_tag.contents[0]

    def _lookup_list_stat(self, dd_tag):
        """Returns the value of a list statistic.

        Some statistics can have multiple values (e.g. the list of characters).
        This helper method should be used to retrieve those.

        """
        # A list tag is stored in the form
        #
        #     <dd class="[field_name] tags">
        #       <ul class="commas">
        #         <li><a href="/further-works">[value 1]</a></li>
        #         <li><a href="/more-info">[value 2]</a></li>
        #         <li class="last"><a href="/more-works">[value 3]</a></li>
        #       </ul>
        #     </dd>
        #
        # We want to get the data from the individual <li> elements.
        li_tags = dd_tag.findAll('li')
        a_tags = [t.contents[0] for t in li_tags]
        return [t.contents[0] for t in a_tags]

    @property
    def rating(self):
        """The age rating for this work."""
        return self._lookup_stat('rating')

    @property
    def warnings(self):
        """Any archive warnings on the work."""
        value = self._lookup_stat('warning')
        if value == ['No Archive Warnings Apply']:
            return []
        else:
            return value

    @property
    def category(self):
        """The category of the work."""
        return self._lookup_stat('category')

    @property
    def fandoms(self):
        """The fandoms in this work."""
        return self._lookup_stat('fandom')

    @property
    def relationship(self):
        """The relationships in this work."""
        return self._lookup_stat('relationship')

    @property
    def characters(self):
        """The characters in this work."""
        return self._lookup_stat('character')

    @property
    def additional_tags(self):
        """Any additional tags on the work."""
        return self._lookup_stat('freeform')

    @property
    def language(self):
        """The language in which this work is published."""
        return self._lookup_stat('language').strip()

    @property
    def published(self):
        """The date when this work was published."""
        date_str = self._lookup_stat('published')
        date_val = datetime.strptime(date_str, '%Y-%m-%d')
        return date_val.date()

    @property
    def words(self):
        """The number of words in this work."""
        return int(self._lookup_stat('words'))

    @property
    def comments(self):
        """The number of comments on this work."""
        return int(self._lookup_stat('comments'))

    @property
    def kudos(self):
        """The number of kudos on this work."""
        return int(self._lookup_stat('kudos'))

    @property
    def kudos_left_by(self):
        """Returns a list of usernames who left kudos on this work."""
        # The list of usernames who left kudos is stored in the following
        # format:
        #
        #     <div id="kudos">
        #       <p class="kudos">
        #         <a href="/users/[username1]">[username1]</a>
        #         <a href="/users/[username2]">[username2]</a>
        #         ...
        #       </p>
        #     </div>
        #
        # And yes, this really does include every username.  The fic with the
        # most kudos is http://archiveofourown.org/works/2080878, and this
        # approach successfully retrieved the username of everybody who
        # left kudos.
        kudos_div = self._soup.find('div', attrs={'id': 'kudos'})
        for a_tag in kudos_div.findAll('a'):

            # If a fic has lots of kudos, not all the users who left kudos
            # are displayed by default.  There's a link for expanding the
            # list of users:
            #
            #     <a href="/works/[work_id]/kudos" id="kudos_summary">
            #
            # and another for collapsing the list afterward:
            #
            #     <a href="#" id="kudos_collapser">
            #
            if a_tag.attrs.get('id') in ('kudos_collapser', 'kudos_summary'):
                continue

            # There's sometimes a kudos summary that can be expanded to

            yield a_tag.attrs['href'].replace('/users/', '')

    @property
    def bookmarks(self):
        """The number of times this work has been bookmarked."""
        # This returns a link of the form
        #
        #     <a href="/works/9079264/bookmarks">102</a>
        #
        # It might be nice to follow that page and get a list of who has
        # bookmarked this, but for now just return the number.
        return int(self._lookup_stat('bookmarks').contents[0])

    @property
    def hits(self):
        """The number of hits this work has received."""
        return int(self._lookup_stat('hits'))

    def json(self, *args, **kwargs):
        """Provide a complete representation of the work in JSON.

        *args and **kwargs are passed directly to `json.dumps()` from the
        standard library.

        """
        data = {
            'id': self.id,
            'title': self.title,
            'author': self.author,
            'summary': self.summary,
            'rating': self.rating,
            'warnings': self.warnings,
            'category': self.category,
            'fandoms': self.fandoms,
            'relationship': self.relationship,
            'characters': self.characters,
            'additional_tags': self.additional_tags,
            'language': self.language,
            'stats': {
                'published': str(self.published),
                'words': self.words,
                # TODO: chapters
                'comments': self.comments,
                'kudos': self.kudos,
                'bookmarks': self.bookmarks,
                'hits': self.hits,
            }
        }
        return json.dumps(data, *args, **kwargs)
