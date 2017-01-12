ao3.py
======

This Python package provides a scripted interface to some of the data on
`AO3 <https://archiveofourown.org/>`_ (the Archive of Our Own).

Because AO3 doesn't have an official API (although `it's on the roadmap
<http://archiveofourown.org/admin_posts/295>`_), this module does some HTML
scraping to retrieve metadata.  I wrote this for some personal scripts as
a stopgap until we get a proper API.

Installation
------------

Install using pip:

.. code-block:: console

  $ pip install ao3

Basic usage
-----------

Create an API instance:

.. code-block:: pycon

   >>> from ao3 import AO3
   >>> api = AO3()

Getting a work:

.. code-block:: pycon

   >>> work = api.work(id='258626')

Looking up metadata on that work:

.. code-block:: pycon

   >>> work.title
   'The Morning After'
   >>> work.author
   'ambyr'

You can see the other attributes using ``dir(work)`` or ``help(work)``.

Feedback/suggestions
--------------------

I'm not putting a lot of time into this, but I have a few ideas (see
`Experiments with AO3 and Python
<https://alexwlchan.net/2017/01/experiments-with-ao3-and-python/>`_).
If there's some part of AO3 you'd really like a scripted interface to,
let me know (`contact details <https://alexwlchan.net/about/>`_) and I'll
give it some thought.

License
-------

The project is licensed under the MIT license.
