import requests
import re
import json

def get_url():
    return f'https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=software+engineer&typedLocation=&locT=N&locId=193&jobType=&context=Jobs&sc.keyword=software+engineer'

class Request():
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
            'AppleWebKit/537.11 (KHTML, like Gecko) '
            'Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        self.session = requests.Session()
    def get(self, url, headers=None, data=None, json=None):
        temp_headers = {k:v for k,v in self.headers.items()}
        if headers:
            for key in headers:
                temp_headers[key] = headers[key]
        return self.session.get(url, headers=temp_headers, data=data, json=json)
    def post(self, url, headers=None, data=None, json=None):
        temp_headers = {k:v for k,v in self.headers.items()}
        if headers:
            for key in headers:
                temp_headers[key] = headers[key]
        return self.session.post(url, headers=temp_headers, data=data, json=json)
  
    def get_location(self, location):
        try:
            location = requests.get(f'https://www.glassdoor.com/findPopularLocationAjax.htm?maxLocationsToReturn=1&term={location}', headers=self.headers).json()[0]
            return location['locationId'], location['locationType']
        except json.decoder.JSONDecodeError:
            print(f"Exception: Unable to find location data for '{location}'")
            exit(0)
        except IndexError:
            print(f"Exception: Unable to find location data for '{location}'")
            exit(0)

def main(query, location):
    # initialise
    session = Request()

    # get location data
    loc_id, loc_type = session.get_location(location)
    #assert loc_id == 96
    #assert loc_type == 'N'

    #loc_id, loc_type = get_location(session,'Taosfijpasodifjaspodfjapoiejfqpoweifpqosjdf;lasjdf')
    #print(loc_id, loc_type)
    #assert loc_id == 96
    #assert loc_type == 'N'

    # get a csrf token

    
    r = session.get(f'https://www.glassdoor.com/Job/jobs.htm?locT={loc_type}&locId={loc_id}&jobType=&context=Jobs&sc.keyword=software+engineer')
    token = [x for x in re.findall('\"gdToken\"\:\"([A-Za-z\-\_0-9\:]*)\"',r.text)][0]
    # print(token)

    # search for jobs
    query = {
        "operationName": "JobSearchQuery",
        "variables": {
            "searchParams": {
                "keyword": "junior developer",
                "numPerPage": 30,
                "searchType": "SR",
                "pageNumber": 1,
                "filterParams": [
                    {
                        "filterKey": "includeNoSalaryJobs",
                        "values": "true"
                    },
                    {
                        "filterKey": "sc.keyword",
                        "values": "junior developer"
                    },
                    {
                        "filterKey": "locT",
                        "values": ""
                    },
                    {
                        "filterKey": "locId",
                        "values": ""
                    }
                ],
                "seoUrl": False
            }
        },
        "query": "query JobSearchQuery($searchParams: SearchParams) {\n  jobListings(contextHolder: {searchParams: $searchParams}) {\n    adOrderJobLinkImpressionTracking\n    totalJobsCount\n    filterOptions\n    companiesLink\n    dataset1\n    indexablePageForSeo\n    searchQueryGuid\n    indeedCtk\n    jobSearchTrackingKey\n    paginationCursors {\n      pageNumber\n      cursor\n      __typename\n    }\n    companyFilterOptions {\n      id\n      shortName\n      __typename\n    }\n    serpSeoLinksVO {\n      relatedJobTitlesResults\n      topCityIdsToNameResults {\n        key\n        value\n        __typename\n      }\n      topEmployerIdsToNameResults {\n        key\n        value\n        __typename\n      }\n      searchedJobTitle\n      searchedKeyword\n      searchedLocationIdAsString\n      searchedLocationType\n      searchedLocationSeoName\n      topEmployerNameResults\n      __typename\n    }\n    jobsPageSeoData {\n      pageTitle\n      pageHeader\n      pageFooterText\n      pageMetaDescription\n      __typename\n    }\n    pageImpressionGuid\n    pageSlotId\n    relatedCompaniesLRP\n    relatedCompaniesZRP\n    relatedJobTitles\n    resourceLink\n    seoTableEnabled\n    jobListingSeoLinks {\n      linkItems {\n        position\n        url\n        __typename\n      }\n      __typename\n    }\n    jobListings {\n      jobview {\n        job {\n          descriptionFragments\n          eolHashCode\n          jobReqId\n          jobSource\n          jobTitleId\n          jobTitleText\n          listingId\n          __typename\n        }\n        jobListingAdminDetails {\n          adOrderId\n          cpcVal\n          importConfigId\n          jobListingId\n          jobSourceId\n          userEligibleForAdminJobDetails\n          __typename\n        }\n        overview {\n          id\n          name\n          shortName\n          squareLogoUrl\n          __typename\n        }\n        gaTrackerData {\n          trackingUrl\n          jobViewDisplayTimeMillis\n          requiresTracking\n          isIndeedJob\n          searchTypeCode\n          pageRequestGuid\n          isSponsoredFromJobListingHit\n          isSponsoredFromIndeed\n          __typename\n        }\n        header {\n          adOrderId\n          advertiserType\n          ageInDays\n          applyUrl\n          easyApply\n          easyApplyMethod\n          employerNameFromSearch\n          jobLink\n          jobCountryId\n          jobResultTrackingKey\n          locId\n          locationName\n          locationType\n          needsCommission\n          normalizedJobTitle\n          organic\n          payPercentile90\n          payPercentile50\n          payPercentile10\n          hourlyWagePayPercentile {\n            payPercentile90\n            payPercentile50\n            payPercentile10\n            __typename\n          }\n          rating\n          salarySource\n          sponsored\n          payPeriod\n          payCurrency\n          savedJobId\n          sgocId\n          categoryMgocId\n          urgencySignal {\n            labelKey\n            messageKey\n            normalizedCount\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }
    '''
    query = {
        "operationName": "JobSearchQuery",
        "variables": {
            "searchParams": {
                "keyword": query,
                "locationId": loc_id,
                "numPerPage": 100,
                "searchType": "SR",
                "pageNumber": 1,
                "filterParams": [
                {
                    "filterKey": "includeNoSalaryJobs",
                    "values": "true"
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
                }],
                "seoUrl": False
            }
        },
        "query": "query JobSearchQuery($searchParams: SearchParams) {\n  jobListings(contextHolder: {searchParams: $searchParams}) {\n    adOrderJobLinkImpressionTracking\n    totalJobsCount\n    filterOptions\n    companiesLink\n    dataset1\n    indexablePageForSeo\n    searchQueryGuid\n    indeedCtk\n    jobSearchTrackingKey\n    paginationCursors {\n      pageNumber\n      cursor\n      __typename\n    }\n    companyFilterOptions {\n      id\n      shortName\n      __typename\n    }\n    serpSeoLinksVO {\n      relatedJobTitlesResults\n      topCityIdsToNameResults {\n        key\n        value\n        __typename\n      }\n      topEmployerIdsToNameResults {\n        key\n        value\n        __typename\n      }\n      searchedJobTitle\n      searchedKeyword\n      searchedLocationIdAsString\n      searchedLocationType\n      searchedLocationSeoName\n      topEmployerNameResults\n      __typename\n    }\n    jobsPageSeoData {\n      pageTitle\n      pageHeader\n      pageFooterText\n      pageMetaDescription\n      __typename\n    }\n    pageImpressionGuid\n    pageSlotId\n    relatedCompaniesLRP\n    relatedCompaniesZRP\n    relatedJobTitles\n    resourceLink\n    seoTableEnabled\n    jobListingSeoLinks {\n      linkItems {\n        position\n        url\n        __typename\n      }\n      __typename\n    }\n    jobListings {\n      jobview {\n        job {\n          descriptionFragments\n          eolHashCode\n          jobReqId\n          jobSource\n          jobTitleId\n          jobTitleText\n          listingId\n          __typename\n        }\n        jobListingAdminDetails {\n          adOrderId\n          cpcVal\n          importConfigId\n          jobListingId\n          jobSourceId\n          userEligibleForAdminJobDetails\n          __typename\n        }\n        overview {\n          id\n          name\n          shortName\n          squareLogoUrl\n          __typename\n        }\n        gaTrackerData {\n          trackingUrl\n          jobViewDisplayTimeMillis\n          requiresTracking\n          isIndeedJob\n          searchTypeCode\n          pageRequestGuid\n          isSponsoredFromJobListingHit\n          isSponsoredFromIndeed\n          __typename\n        }\n        header {\n          adOrderId\n          advertiserType\n          ageInDays\n          applyUrl\n          easyApply\n          easyApplyMethod\n          employerNameFromSearch\n          jobLink\n          jobCountryId\n          jobResultTrackingKey\n          locId\n          locationName\n          locationType\n          needsCommission\n          normalizedJobTitle\n          organic\n          payPercentile90\n          payPercentile50\n          payPercentile10\n          hourlyWagePayPercentile {\n            payPercentile90\n            payPercentile50\n            payPercentile10\n            __typename\n          }\n          rating\n          salarySource\n          sponsored\n          payPeriod\n          payCurrency\n          savedJobId\n          sgocId\n          categoryMgocId\n          urgencySignal {\n            labelKey\n            messageKey\n            normalizedCount\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"
    }'''

    job_results = session.post("https://www.glassdoor.com/graph", headers={'gd-csrf-token': token, 'content-type': 'application/json'}, json=query).json()
    total_jobs_count = job_results['data']['jobListings']['totalJobsCount']
    job_listings = job_results['data']['jobListings']['jobListings']
    for x in job_listings:
        job = x['jobview']
        print(job['overview']['name'], job['job']['listingId'], job['header']['locationName'])


    job = job_listings[10]['jobview']['job']
    #print(job_listings[10]['jobview'])
    print()
    print()
    query = {
        "operationName": "JobDetailQuery",
        "variables": {
            "enableReviewSummary": True,
            "jl": job['listingId'],
            "queryString": f"pos=101&ao=1110586&s=58&guid=0000017d8c5c314f85c1c7c517f013ef&src=GD_JOB_AD&t=SR&vt=w&cs=1_1b86b2bd&cb=1638737392276&jobListingId={job['listingId']}"
            # &cpc=8AC01DCC8FF2DC38
            # &jrtk=3-0-1fm65occbu2b8801-1fm65occnu4n8800-03e4bb15d35c5edc--6NYlbfkN0BMvOi78eJGfSGsvuq62vzZL5BIoSWoRDlO9S368Ce2EWls3RzyhmsPYu2QPoXj3I858ZQkOow1pLkw29x4lcawL9HF08zb_B8fwdTnJ-6avry0O644TnRquM95AJAQcV18hpH2KJ9pOMj-chJX5BUXKnwS7BdZATlLNhVwKAazl6ZmFOtXJmCaELbdtPKYdSR2VqKShMgqz6tRvJnHDdbGoY8YvS9hDYNxGbrziBQVmmNP__KoZm9wht4vN99N-KSbeVcj2EBsuvHA_loEqQ3yCV-Qu-VOZBtawm4MDfpXIsSW9AqrSogeaAolKJNUTolxSq2DIrfmESq2XXtyjhYJMPX3-HkT4LigznDlE6zLzBmr3I7S-3zt_iRkO8abR4gCk1YI1bKCKPmx_Aiw5cJE3aJgLxjgk--MbIk8xXAzafdGYx0WXVITEpec5vsSx4KMEL9UNuXXUYOS9iI-FX_MvfKU1CPRrSwa6hmRJuVk221DcN9y_sB3
        },
        "query": "query JobDetailQuery($jl: Long!, $queryString: String, $enableReviewSummary: Boolean!) {\n  jobView(listingId: $jl, contextHolder: {queryString: $queryString}) {\n    ...DetailFragment\n    employerReviewSummary @include(if: $enableReviewSummary) {\n      reviewSummary {\n        highlightSummary {\n          sentiment\n          sentence\n          categoryReviewCount\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment DetailFragment on JobView {\n  employerBenefits {\n    benefitsOverview {\n      benefitsHighlights {\n        benefit {\n          commentCount\n          icon\n          name\n          __typename\n        }\n        highlightPhrase\n        __typename\n      }\n      overallBenefitRating\n      employerBenefitSummary {\n        comment\n        __typename\n      }\n      __typename\n    }\n    benefitReviews {\n      benefitComments {\n        id\n        comment\n        __typename\n      }\n      cityName\n      createDate\n      currentJob\n      rating\n      stateName\n      userEnteredJobTitle\n      __typename\n    }\n    numReviews\n    __typename\n  }\n  employerContent {\n    featuredVideoLink\n    managedContent {\n      id\n      type\n      title\n      body\n      captions\n      photos\n      videos\n      __typename\n    }\n    diversityContent {\n      goals {\n        id\n        workPopulation\n        underRepresentedGroup\n        currentMetrics\n        currentMetricsDate\n        representationGoalMetrics\n        representationGoalMetricsDate\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  employerAttributes {\n    attributes {\n      attributeName\n      attributeValue\n      __typename\n    }\n    __typename\n  }\n  header {\n    jobLink\n    adOrderId\n    advertiserType\n    ageInDays\n    applicationId\n    appliedDate\n    applyUrl\n    applyButtonDisabled\n    blur\n    coverPhoto {\n      url\n      __typename\n    }\n    divisionEmployerName\n    easyApply\n    easyApplyMethod\n    employerNameFromSearch\n    employer {\n      id\n      name\n      size\n      squareLogoUrl\n      __typename\n    }\n    expired\n    goc\n    hideCEOInfo\n    indeedApplyMetadata\n    indeedJobAttribute {\n      education\n      skills\n      __typename\n    }\n    jobTitleText\n    jobTypeKeys\n    jobCountryId\n    jobResultTrackingKey\n    locId\n    locationName\n    locationType\n    normalizedJobTitle\n    organic\n    payCurrency\n    payPercentile90\n    payPercentile50\n    payPercentile10\n    hourlyWagePayPercentile {\n      payPercentile90\n      payPercentile50\n      payPercentile10\n      __typename\n    }\n    payPeriod\n    rating\n    salarySource\n    savedJobId\n    sgocId\n    sponsored\n    categoryMgocId\n    urgencySignal {\n      labelKey\n      messageKey\n      normalizedCount\n      __typename\n    }\n    __typename\n  }\n  similarJobs {\n    relatedJobTitle\n    careerUrl\n    __typename\n  }\n  job {\n    description\n    discoverDate\n    eolHashCode\n    importConfigId\n    jobReqId\n    jobSource\n    jobTitleId\n    jobTitleText\n    listingId\n    __typename\n  }\n  map {\n    address\n    country\n    employer {\n      id\n      name\n      __typename\n    }\n    locationName\n    postalCode\n    __typename\n  }\n  overview {\n    ceo {\n      name\n      photoUrl\n      __typename\n    }\n    id\n    name\n    shortName\n    squareLogoUrl\n    headquarters\n    links {\n      overviewUrl\n      benefitsUrl\n      photosUrl\n      reviewsUrl\n      salariesUrl\n      __typename\n    }\n    primaryIndustry {\n      industryId\n      industryName\n      sectorName\n      sectorId\n      __typename\n    }\n    ratings {\n      compensationAndBenefitsRating\n      cultureAndValuesRating\n      careerOpportunitiesRating\n      workLifeBalanceRating\n      __typename\n    }\n    overview {\n      description\n      __typename\n    }\n    revenue\n    size\n    type\n    website\n    yearFounded\n    __typename\n  }\n  photos {\n    photos {\n      caption\n      photoId\n      photoId2x\n      photoLink\n      photoUrl\n      photoUrl2x\n      __typename\n    }\n    __typename\n  }\n  rating {\n    ceoApproval\n    ceoRatingsCount\n    employer {\n      name\n      __typename\n    }\n    recommendToFriend\n    starRating\n    __typename\n  }\n  reviews {\n    reviews {\n      advice\n      cons\n      countHelpful\n      employerResponses {\n        response\n        responseDateTime\n        userJobTitle\n        __typename\n      }\n      employmentStatus\n      featured\n      isCurrentJob\n      jobTitle {\n        text\n        __typename\n      }\n      lengthOfEmployment\n      pros\n      ratingBusinessOutlook\n      ratingCareerOpportunities\n      ratingCeo\n      ratingCompensationAndBenefits\n      ratingCultureAndValues\n      ratingOverall\n      ratingRecommendToFriend\n      ratingSeniorLeadership\n      ratingWorkLifeBalance\n      reviewDateTime\n      reviewId\n      summary\n      __typename\n    }\n    __typename\n  }\n  salary {\n    currency {\n      code\n      numOfDecimals\n      negativeFormat\n      positiveFormat\n      symbol\n      __typename\n    }\n    lastSalaryDate\n    salaries {\n      count\n      maxBasePay\n      medianBasePay\n      minBasePay\n      jobTitle {\n        id\n        text\n        __typename\n      }\n      payPeriod\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n"
    }
    result = session.post("https://www.glassdoor.com/graph", headers={'gd-csrf-token': token, 'content-type': 'application/json'}, json=query).json()
    #print(result['data']['jobView']['job'])

if __name__ == "__main__":
    main('Junior Web Developer', 'Poland')

    '''




    r = session.post("https://www.glassdoor.com/graph", headers=headers, json=query)
    print(r.json()['data']['jobListings']['jobListings'][0])
    print(r.json()['data']['jobListings']['totalJobsCount'])
    #print(r.json()['data']['jobView']['overview']['name'])
    '''
