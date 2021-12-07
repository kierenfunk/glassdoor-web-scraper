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


def test_csrf_token():
    """Testing csrf token initialisation

    """
    session = Request()
    assert 'gd-csrf-token' in session.headers
    assert len(session.headers['gd-csrf-token']) > 0


def test_get_job_listings():
    """Testing job listing getter

    """
    session = Request()
    response = session.get_job_listings('Junior Web Developer', 'Berlin')
    assert response['data']['jobListings']['totalJobsCount'] > 0
    assert len(response['data']['jobListings']['jobListings']) == 100


def test_get_job_details():
    """Testing job details getter

    """
    session = Request()
    response = session.get_job_listings('Junior Web Developer', 'Berlin')
    job = response['data']['jobListings']['jobListings'][0]
    listing_id = job['jobview']['job']['listingId']
    job_response = session.get_job_details(listing_id)
    assert job_response is not None
