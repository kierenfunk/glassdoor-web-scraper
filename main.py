"""Glassdoor web scraper

"""

import re
import json
import sys
import requests
import queries


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

    def get(self, url, headers=None, data=None):
        """Get request with session

        """
        temp_headers = self.headers
        if headers:
            for key in headers:
                temp_headers[key] = headers[key]
        return self.session.get(url, headers=temp_headers, data=data)

    def post(self, url, headers=None, data=None, json_arg=None):
        """Post request with session

        """
        temp_headers = self.headers
        if headers:
            for key in headers:
                temp_headers[key] = headers[key]
        return self.session.post(url,
                                 headers=temp_headers,
                                 data=data,
                                 json=json_arg)

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

    # get location data
    loc_id, loc_type = session.get_location(location)
    # assert loc_id == 96
    # assert loc_type == 'N'

    # loc_id, loc_type = get_location('Taosfijpasodifjaspodfjapoiej')
    # print(loc_id, loc_type)
    # assert loc_id == 96
    # assert loc_type == 'N'

    # get a csrf token

    response = session.get(
        ('https://www.glassdoor.com/Job/jobs.htm?'
         f'locT={loc_type}&locId={loc_id}'
         '&jobType=&context=Jobs&sc.keyword=software+engineer'))
    token = list(re.findall(
        r'\"gdToken\"\:\"([A-Za-z\-\_0-9\:]*)\"', response.text))[0]
    # print(token)

    # search for jobs
    location_type = {
        'N': 'COUNTRY',
        'C': 'CITY'
    }
    query = {
        "operationName": "JobSearchQuery",
        "variables": {
            "searchParams": {
                "keyword": query,
                "locationId": loc_id,
                "locationType": location_type[loc_type],
                "numPerPage": 100,
                "searchType": "SR",
                "pageNumber": 1,
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

    job_results = session.post("https://www.glassdoor.com/graph",
                               headers={
                                   'gd-csrf-token': token,
                                   'content-type': 'application/json'},
                               json_arg=query).json()
    total_jobs_count = job_results['data']['jobListings']['totalJobsCount']
    job_listings = job_results['data']['jobListings']['jobListings']
    for job in job_listings:
        job = job['jobview']
        print(job['overview']['name'], job['job']
              ['listingId'], job['header']['locationName'])

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


if __name__ == "__main__":
    pass
    # main('Junior Developer', 'Berlin')
