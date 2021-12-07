"""Glassdoor web scraper testing

"""

import pytest
from main import Request


def test_get_location():
    """Get location method tests

    - tests that it correctly returns a city and country
    - tests sys exit when no input is given
    - tests sys exit when input is given that results in no result
    """
    session = Request()
    loc_id, loc_type = session.get_location('Germany')
    assert loc_id == 96
    assert loc_type == 'N'

    loc_id, loc_type = session.get_location('Berlin')
    assert loc_id == 2622109
    assert loc_type == 'C'

    with pytest.raises(SystemExit):
        session.get_location('Taosfijpasodifjaspodfjapoiej')
    with pytest.raises(SystemExit):
        session.get_location('')
