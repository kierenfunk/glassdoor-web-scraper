"""Contains string constants for glassdoor's graphql backend

"""

JOB_SEARCH_QUERY = '''query JobSearchQuery($searchParams: SearchParams) {
  jobListings(contextHolder: {searchParams: $searchParams}) {
    adOrderJobLinkImpressionTracking
    totalJobsCount
    filterOptions
    companiesLink
    dataset1
    indexablePageForSeo
    searchQueryGuid
    indeedCtk
    jobSearchTrackingKey
    paginationCursors {
      pageNumber
      cursor
      __typename
    }
    companyFilterOptions {
      id
      shortName
      __typename
    }
    serpSeoLinksVO {
      relatedJobTitlesResults
      topCityIdsToNameResults {
        key
        value
        __typename
      }
      topEmployerIdsToNameResults {
        key
        value
        __typename
      }
      searchedJobTitle
      searchedKeyword
      searchedLocationIdAsString
      searchedLocationType
      searchedLocationSeoName
      topEmployerNameResults
      __typename
    }
    jobsPageSeoData {
      pageTitle
      pageHeader
      pageFooterText
      pageMetaDescription
      __typename
    }
    pageImpressionGuid
    pageSlotId
    relatedCompaniesLRP
    relatedCompaniesZRP
    relatedJobTitles
    resourceLink
    seoTableEnabled
    jobListingSeoLinks {
      linkItems {
        position
        url
        __typename
      }
      __typename
    }
    jobListings {
      jobview {
        job {
          descriptionFragments
          eolHashCode
          jobReqId
          jobSource
          jobTitleId
          jobTitleText
          listingId
          __typename
        }
        jobListingAdminDetails {
          adOrderId
          cpcVal
          importConfigId
          jobListingId
          jobSourceId
          userEligibleForAdminJobDetails
          __typename
        }
        overview {
          id
          name
          shortName
          squareLogoUrl
          __typename
        }
        gaTrackerData {
          trackingUrl
          jobViewDisplayTimeMillis
          requiresTracking
          isIndeedJob
          searchTypeCode
          pageRequestGuid
          isSponsoredFromJobListingHit
          isSponsoredFromIndeed
          __typename
        }
        header {
          adOrderId
          advertiserType
          ageInDays
          applyUrl
          easyApply
          easyApplyMethod
          employerNameFromSearch
          jobLink
          jobCountryId
          jobResultTrackingKey
          locId
          locationName
          locationType
          needsCommission
          normalizedJobTitle
          organic
          payPercentile90
          payPercentile50
          payPercentile10
          hourlyWagePayPercentile {
            payPercentile90
            payPercentile50
            payPercentile10
            __typename
          }
          rating
          salarySource
          sponsored
          payPeriod
          payCurrency
          savedJobId
          sgocId
          categoryMgocId
          urgencySignal {
            labelKey
            messageKey
            normalizedCount
            __typename
          }
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}'''

JOB_DETAIL_QUERY = (
    'query JobDetailQuery($jl: Long!, $queryString: '
    'String, $enableReviewSummary: Boolean!) {'
    '''jobView(listingId: $jl, contextHolder: {queryString: $queryString}) {
    ...DetailFragment
    employerReviewSummary @include(if: $enableReviewSummary) {
      reviewSummary {
        highlightSummary {
          sentiment
          sentence
          categoryReviewCount
          __typename
        }
        __typename
      }
      __typename
    }
    __typename
  }
}

fragment DetailFragment on JobView {
  employerBenefits {
    benefitsOverview {
      benefitsHighlights {
        benefit {
          commentCount
          icon
          name
          __typename
        }
        highlightPhrase
        __typename
      }
      overallBenefitRating
      employerBenefitSummary {
        comment
        __typename
      }
      __typename
    }
    benefitReviews {
      benefitComments {
        id
        comment
        __typename
      }
      cityName
      createDate
      currentJob
      rating
      stateName
      userEnteredJobTitle
      __typename
    }
    numReviews
    __typename
  }
  employerContent {
    featuredVideoLink
    managedContent {
      id
      type
      title
      body
      captions
      photos
      videos
      __typename
    }
    diversityContent {
      goals {
        id
        workPopulation
        underRepresentedGroup
        currentMetrics
        currentMetricsDate
        representationGoalMetrics
        representationGoalMetricsDate
        __typename
      }
      __typename
    }
    __typename
  }
  employerAttributes {
    attributes {
      attributeName
      attributeValue
      __typename
    }
    __typename
  }
  header {
    jobLink
    adOrderId
    advertiserType
    ageInDays
    applicationId
    appliedDate
    applyUrl
    applyButtonDisabled
    blur
    coverPhoto {
      url
      __typename
    }
    divisionEmployerName
    easyApply
    easyApplyMethod
    employerNameFromSearch
    employer {
      id
      name
      size
      squareLogoUrl
      __typename
    }
    expired
    goc
    hideCEOInfo
    indeedApplyMetadata
    indeedJobAttribute {
      education
      skills
      __typename
    }
    jobTitleText
    jobTypeKeys
    jobCountryId
    jobResultTrackingKey
    locId
    locationName
    locationType
    normalizedJobTitle
    organic
    payCurrency
    payPercentile90
    payPercentile50
    payPercentile10
    hourlyWagePayPercentile {
      payPercentile90
      payPercentile50
      payPercentile10
      __typename
    }
    payPeriod
    rating
    salarySource
    savedJobId
    sgocId
    sponsored
    categoryMgocId
    urgencySignal {
      labelKey
      messageKey
      normalizedCount
      __typename
    }
    __typename
  }
  similarJobs {
    relatedJobTitle
    careerUrl
    __typename
  }
  job {
    description
    discoverDate
    eolHashCode
    importConfigId
    jobReqId
    jobSource
    jobTitleId
    jobTitleText
    listingId
    __typename
  }
  map {
    address
    country
    employer {
      id
      name
      __typename
    }
    locationName
    postalCode
    __typename
  }
  overview {
    ceo {
      name
      photoUrl
      __typename
    }
    id
    name
    shortName
    squareLogoUrl
    headquarters
    links {
      overviewUrl
      benefitsUrl
      photosUrl
      reviewsUrl
      salariesUrl
      __typename
    }
    primaryIndustry {
      industryId
      industryName
      sectorName
      sectorId
      __typename
    }
    ratings {
      compensationAndBenefitsRating
      cultureAndValuesRating
      careerOpportunitiesRating
      workLifeBalanceRating
      __typename
    }
    overview {
      description
      __typename
    }
    revenue
    size
    type
    website
    yearFounded
    __typename
  }
  photos {
    photos {
      caption
      photoId
      photoId2x
      photoLink
      photoUrl
      photoUrl2x
      __typename
    }
    __typename
  }
  rating {
    ceoApproval
    ceoRatingsCount
    employer {
      name
      __typename
    }
    recommendToFriend
    starRating
    __typename
  }
  reviews {
    reviews {
      advice
      cons
      countHelpful
      employerResponses {
        response
        responseDateTime
        userJobTitle
        __typename
      }
      employmentStatus
      featured
      isCurrentJob
      jobTitle {
        text
        __typename
      }
      lengthOfEmployment
      pros
      ratingBusinessOutlook
      ratingCareerOpportunities
      ratingCeo
      ratingCompensationAndBenefits
      ratingCultureAndValues
      ratingOverall
      ratingRecommendToFriend
      ratingSeniorLeadership
      ratingWorkLifeBalance
      reviewDateTime
      reviewId
      summary
      __typename
    }
    __typename
  }
  salary {
    currency {
      code
      numOfDecimals
      negativeFormat
      positiveFormat
      symbol
      __typename
    }
    lastSalaryDate
    salaries {
      count
      maxBasePay
      medianBasePay
      minBasePay
      jobTitle {
        id
        text
        __typename
      }
      payPeriod
      __typename
    }
    __typename
  }
  __typename
}''')
