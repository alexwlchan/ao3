# -*- encoding: utf-8
"""Tests for ao3.utils."""

import pytest

from ao3 import utils


@pytest.mark.parametrize('url, work_id', [
    ('https://archiveofourown.org/works/1', '1'),
    ('https://archiveofourown.org/works/1234567', '1234567'),
    ('https://archiveofourown.org/works/1?view_adult=true', '1'),
    ('https://archiveofourown.org/works/1234567?view_adult=true', '1234567'),
    ('http://archiveofourown.org/works/1?view_adult=true', '1'),
    ('http://archiveofourown.org/works/1234567?view_adult=true', '1234567'),
])
def test_work_id_from_url(url, work_id):
    assert utils.work_id_from_url(url) == work_id


@pytest.mark.parametrize('bad_url', [
    'http://google.co.uk',
    'http://archiveofourown.org/users/username',
])
def test_work_id_from_bad_url_raises_runtimeerror(bad_url):
    """Trying to get a work ID from a non-work URL raises a RuntimeError."""
    with pytest.raises(RuntimeError) as exc:
        utils.work_id_from_url(bad_url)
    assert 'not a recognised AO3 work URL' in exc.value.message
