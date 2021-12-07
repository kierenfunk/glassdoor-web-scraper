"""Glassdoor web scraper

"""

import re
import json
import sys
import requests
import queries


def get_job_search_query(query, loc_id, loc_type, count=100, page=1):
    """Get graphql query for JobSearch

    """
    location_types = {
        'N': 'COUNTRY',
        'C': 'CITY'
    }
    return {
        "operationName": "JobSearchQuery",
        "variables": {
            "searchParams": {
                "keyword": query,
                "locationId": loc_id,
                "locationType": location_types[loc_type],
                "numPerPage": count,
                "searchType": "SR",
                "pageNumber": page,
                "filterParams": [
                    {
                        "filterKey": "sortBy",
                        "values": "date_desc"
                    },
                    {
                        "filterKey": "sc.keyword",
                        "values": query
                    },
                    {
                        "filterKey": "locT",
                        "values": loc_type
                    },
                    {
                        "filterKey": "locId",
                        "values": str(loc_id)
                    }
                ],
                "seoUrl": False
            }
        },
        "query": queries.JOB_SEARCH_QUERY
    }


class Request():
    """Request class for handling session requests

    """

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.11 (KHTML, like Gecko) '
            'Chrome/23.0.1271.64 Safari/537.11',
            'Accept': ('text/html,application/xhtml'
                       '+xml,application/xml;q=0.9,*/*;q=0.8'),
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        self.session = requests.Session()
        self.set_csrf()

    def set_csrf(self):
        """Set the csrf header on initialisation

        """
        response = self.session.get('https://www.glassdoor.com/Job/jobs.htm',
                                    headers=self.headers)
        # get csrf token
        token = list(re.findall(
            r'\"gdToken\"\:\"([A-Za-z\-\_0-9\:]*)\"', response.text))[0]
        self.headers['gd-csrf-token'] = token

    def get_job_listings(self, query, location):
        """Get a list of job listings

        """
        loc_id, loc_type = self.get_location(location)
        return self.session.post(
            "https://www.glassdoor.com/graph",
            headers={**self.headers,
                     'content-type': 'application/json'},
            json=get_job_search_query(
                query, loc_id, loc_type)
        ).json()

    def get_location(self, location):
        """Get location from a location string using glassdoor function

        """
        try:
            location = requests.get(
                ('https://www.glassdoor.com/findPopularLocationAjax.htm?'
                 f'maxLocationsToReturn=1&term={location}'),
                headers=self.headers
            ).json()[0]
            return location['locationId'], location['locationType']
        except json.decoder.JSONDecodeError:
            print(f"Exception: Unable to find location data for '{location}'")
            sys.exit(0)
        except IndexError:
            print(f"Exception: Unable to find location data for '{location}'")
            sys.exit(0)


def main(query, location):
    """main function

    """
    # initialise
    session = Request()
    response = session.get_job_listings(query, location)
    print(response)
    '''
    print(total_jobs_count)
    job = job_listings[0]['jobview']['job']
    print()
    print()
    query = {
        "operationName": "JobDetailQuery",
        "variables": {
            "enableReviewSummary": True,
            "jl": job['listingId'],
            "queryString": ("pos=101&ao=1110586&s=58&guid"
                            "=0000017d8c5c314f85c1c7c517f013ef&t=SR&vt=w&"
                            f"cs=1_1b86b2bd&jobListingId={job['listingId']}")
        },
        "query": queries.JOB_DETAIL_QUERY
    }

    result = session.post("https://www.glassdoor.com/graph",
                          headers={
                              'gd-csrf-token': token,
                              'content-type': 'application/json'},
                          json_arg=query).json()
    print(json.dumps(result['data']['jobView'], sort_keys=True, indent=2))
    '''


if __name__ == "__main__":
    main('Junior Developer', 'Berlin')
