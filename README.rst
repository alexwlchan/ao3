**Maintenance note, 19 July 2020:** This isn't actively maintained, and it hasn't been for a long time.
I created this library/repo to accompany a `blog post I wrote in 2018 <https://alexwlchan.net/2017/01/scrape-logged-in-ao3/>`_, but I haven't looked at it much since then and I don't have much time for open source these days.

FWIW, if I were to work on this again, I'd start by decoupling the HTML parsing and the I/O logic (see my PyCon UK talk about `sans I/O programming <https://alexwlchan.net/2019/10/sans-io-programming/>`_).

I hope this repo serves as a useful pointer, but don't expect updates any time soon.

----

ao3.py
======

This Python package provides a scripted interface to some of the data on
`AO3 <https://archiveofourown.org/>`_ (the Archive of Our Own).

It is **not** an official API.

Motivation
**********

I want to be able to write Python scripts that use data from AO3.

An official API for AO3 data has been `on the roadmap <http://archiveofourown.org/admin_posts/295>`_
for a couple of years.  Until that appears, I've cobbled together my own
page-scraping code that does the job.  It's a bit messy and fragile, but it
seems to work most of the time.

If/when we get the proper API, I'd drop this in a heartbeat and do it
properly.

Installation
************

Install using pip:

.. code-block:: console

   $ pip install ao3

I'm trying to support Python 2.7, Python 3.3+ and PyPy.

Usage
*****

Create an API instance:

.. code-block:: pycon

   >>> from ao3 import AO3, 
   >>> api = AO3()

Looking up information about a work
-----------------------------------

Getting a work:

.. code-block:: pycon

   >>> work = api.work(id='258626')

The ``id`` is the numeric portion of the URL.  For example, the work ID of
``https://archiveofourown.org/works/258626`` is ``258626``.

Get a URL:

.. code-block:: pycon

   >>> work.url
   'https://archiveofourown.org/works/258626'

You can then look up a number of attributes, similar to the Stats panel at the
top of a page.  Here's the full set you can look up:

.. code-block:: pycon

   >>> work.title
   'The Morning After'

   >>> work.author
   'ambyr'

   >>> work.summary
   "<p>Delicious just can't understand why it's the shy, quiet ones who get all the girls.</p>"

   >>> work.rating
   ['Teen And Up Audiences']

   >>> work.warnings
   []

(An empty list is synonymous with "No Archive Warnings", so that it's a falsey
value.)

.. code-block:: pycon

   >>> work.category
   ['F/M']

   >>> work.fandoms
   ['Anthropomorfic - Fandom']

   >>> work.relationship
   ['Pinboard/Fandom']

   >>> work.characters
   ['Pinboard', 'Delicious - Character', 'Diigo - Character']

   >>> work.additional_tags
   ['crackfic', 'Meta', 'so very not my usual thing']

   >>> work.language
   'English'

   >>> work.published
   datetime.date(2011, 9, 29)

   >>> work.words
   605

   >>> work.comments
   122

   >>> work.kudos
   1238

   >>> for name in work.kudos_left_by:
   ...     print(name)
   ...
   winterbelles
   AnonEhouse
   SailAweigh
   # and so on

   >>> work.bookmarks
   99

   >>> work.hits
   43037

There's also a method for dumping all the information about a work into JSON,
for easy export/passing into other places:

.. code-block:: pycon

   >>> work.json()
   '{"rating": ["Teen And Up Audiences"], "fandoms": ["Anthropomorfic - Fandom"], "characters": ["Pinboard", "Delicious - Character", "Diigo - Character"], "language": "English", "additional_tags": ["crackfic", "Meta", "so very not my usual thing"], "warnings": [], "id": "258626", "stats": {"hits": 43037, "words": 605, "bookmarks": 99, "comments": 122, "published": "2011-09-29", "kudos": 1238}, "author": "ambyr", "category": ["F/M"], "title": "The Morning After", "relationship": ["Pinboard/Fandom"], "summary": "<p>Delicious just can\'t understand why it\'s the shy, quiet ones who get all the girls.</p>"}'

Looking up your account
-----------------------

If you have an account on AO3, you can log in to access pages that aren't
available to the public:

.. code-block:: pycon

   >>> api.login('username', 'password')

If you have Viewing History enabled, you can get a list of work IDs from 
that history, like so:

.. code-block:: pycon

   >>> for entry in api.user.reading_history():
   ...     print(entry.work_id)
   ...
   '123'
   '456'
   '789'
   # and so on

You can enable Viewing History in the settings pane.

One interesting side effect of this is that you can use it to get a list
of works where you've left kudos:

.. code-block:: python

   from ao3 import AO3
   from ao3.works import RestrictedWork

   api = AO3()
   api.login('username', 'password')

   for entry in api.user.reading_history():
       try:
           work = api.work(id=entry.work_id)
       except RestrictedWork:
           continue
       print(work.url + '... ', end='')
       if api.user.username in work.kudos_left_by:
           print('yes')
       else:
           print('no')

Warning: this is `very` slow.  It has to go back and load a page for everything
you've ever read.  Don't use this if you're on a connection with limited
bandwidth.

This doesn't include "restricted" works -- works that require you to be a
logged-in user to see them.

(The reading page tells you when you last read something.  If you cached the
results, and then subsequent runs only rechecked fics you'd read since the
last run, you could make this quite efficient.  Exercise for the reader.)

Looking up your bookmarks
-------------------------

If you login as a user you can look up the bookmarks for that user. You can 
get the bookmarks as a list of AO3 id numbers or as a list of work objects.

Warning: This is very slow as as the api has to go back and retrieve every 
page.

Get the bookmarks as works:

.. code-block:: pycon

   >>> for bookmark in api.user.bookmarks():
   ...     print(bookmark.title)
   ...
   'Story Name'
   'Fanfiction Title'
   'Read This Fic'
   # and so on

Get the bookmarks as a list of id numbers:

.. code-block:: pycon

   >>> for bookmark_id in api.user.bookmarks_ids():
   ...     print(bookmark_id)
   ...
   '123'
   '456'
   '789'
   # and so on



License
*******

The project is licensed under the MIT license.
