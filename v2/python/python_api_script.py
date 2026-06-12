# Script for pulling data from the Finaeon API v2
# Authenticates with an API key in the X-Api-Key header.
# API keys can be managed from the Self-Service Portal (https://app.finaeon.com/).

import requests
import pandas as pd
import os
import json
from datetime import datetime
import traceback

Finaeon_API_URL = "https://api.finaeon.com"
# Trial API key. Replace with your own API key from the Self-Service Portal.
Finaeon_API_KEY = ""

def writeJSONToFile(fileSuffix, jsonContents):
    now = datetime.now()
    jsonFilename = now.strftime("%Y%m%d-%H%M%S%f") + '_' + fileSuffix + '.json'
    relativeDirectory = './responses/'
    if not os.path.isdir(relativeDirectory):
        os.mkdir(relativeDirectory)
    outputfilepath = relativeDirectory + jsonFilename
    with open(outputfilepath, 'w') as f:
        json.dump(jsonContents, f)

def call_api(path, parameters):
    url = Finaeon_API_URL + path
    headers = {'Content-Type': 'application/json',
               'X-Api-Key': Finaeon_API_KEY}
    print("calling %s" % url)
    print("request body: \r\n %s" % parameters)
    writeJSONToFile(path.strip('/').replace('/', '_') + 'Request', parameters)
    resp = requests.post(url, headers=headers, data=json.dumps(parameters))
    if resp.status_code != 200:
        raise ValueError('Finaeon API request to %s failed with HTTP status code %s: %s'
                         % (path, resp.status_code, resp.text))
    return resp

def finaeon_search(searchString, **kwargs):
    page = kwargs.get('page', None)
    pageSize = kwargs.get('pageSize', None)
    searchType = kwargs.get('searchType', None)
    baseFilter = kwargs.get('baseFilter', None)
    sort = kwargs.get('sort', None)
    parameters = {"page": page,
                  "pageSize": pageSize,
                  "searchString": searchString,
                  "searchType": searchType,
                  "baseFilter": baseFilter,
                  "sort": sort
                  }
    parameters = {key: val for key, val in parameters.items() if val != None}
    r = call_api('/v2/search', parameters=parameters)
    search_data = r.json()
    return search_data

def finaeon_searchbycikcodes(cikCodes):
    parameters = {"cikCodes": cikCodes}
    r = call_api('/v2/searchbycikcodes', parameters)
    searchbycikcodes_data = r.json()
    return searchbycikcodes_data

def finaeon_series(**kwargs):
    seriesId = kwargs.get('seriesId', None)
    seriesName = kwargs.get('seriesName', None)
    splitAdjusted = kwargs.get('splitAdjusted', None)
    startDate = kwargs.get('startDate', None)
    endDate = kwargs.get('endDate', None)
    periodicity = kwargs.get('periodicity', None)
    closeOnly = kwargs.get('closeOnly', None)
    currency = kwargs.get('currency', None)
    inflationAdjusted = kwargs.get('inflationAdjusted', None)
    annualFlow = kwargs.get('annualFlow', None)
    totalReturn = kwargs.get('totalReturn', None)
    corporateActions = kwargs.get('corporateActions', None)
    metadata = kwargs.get('metadata', None)
    incFields = kwargs.get('incFields', None)
    includeAverage = kwargs.get('includeAverage', None)
    periodPercentChange = kwargs.get('periodPercentChange', None)
    annualPercentChange = kwargs.get('annualPercentChange', None)
    pointInTime = kwargs.get('pointInTime', None)
    parameters = {"seriesId": seriesId,
                  "seriesName": seriesName,
                  "splitAdjusted": splitAdjusted,
                  "startDate": startDate,
                  "endDate": endDate,
                  "periodicity": periodicity,
                  "closeOnly": closeOnly,
                  "currency": currency,
                  "inflationAdjusted": inflationAdjusted,
                  "annualFlow": annualFlow,
                  "totalReturn": totalReturn,
                  "corporateActions": corporateActions,
                  "metadata": metadata,
                  "incFields": incFields,
                  "includeAverage": includeAverage,
                  "periodPercentChange": periodPercentChange,
                  "annualPercentChange": annualPercentChange,
                  "pointInTime": pointInTime
                  }

    parameters = {key: val for key, val in parameters.items() if val != None}
    r = call_api('/v2/series', parameters=parameters)
    series_data = r.json()
    return series_data

def finaeon_fundamentals(seriesName, period, **kwargs):
    startDate = kwargs.get('startDate', None)
    endDate = kwargs.get('endDate', None)
    group = kwargs.get('group', None)
    parameters = {"seriesName": seriesName,
                  "period": period,
                  "startDate": startDate,
                  "endDate": endDate,
                  "group": group
                  }
    parameters = {key: val for key, val in parameters.items() if val != None}
    r = call_api('/v2/fundamentals', parameters)
    fundamentals_data = r.json()
    return fundamentals_data


try:
    # series API call
    series_price_data = finaeon_series(seriesName="IBM", startDate="01/01/2019", closeOnly="true", periodicity="monthly")
    writeJSONToFile('series_price_data', series_price_data)
    data = pd.DataFrame(series_price_data['price_data'])
    print(data)

    # search API call
    search_info = finaeon_search(searchString="MSFT", searchType="symbol", baseFilter="startsWith")
    # search_info = finaeon_search(searchString="General Motors", searchType="name", baseFilter="contains")
    # search_info = finaeon_search(searchString="General Motors", searchType="name", baseFilter="contains", sort="pop", page="3", pageSize="10")
    writeJSONToFile('search_info', search_info)

    # use dictionary comp to build a dict keyed by symbol
    search_dict = {s["symbol"]: s for s in search_info["search_results"]}
    print('symbols found:', list(search_dict.keys()))

    # search by cik API call
    search_info_by_cik = finaeon_searchbycikcodes(cikCodes="0000354950,0000789019")
    writeJSONToFile('search_info_by_cik', search_info_by_cik)
    print(search_info_by_cik)

    # fundamentals API call
    # NOTE: requires a subscription with fundamentals access -
    # the trial API key will receive a 401 response.
    fundamentals_info = finaeon_fundamentals(seriesName="MSFT", period="Annual", group="Balance Sheet", startDate="01/01/2010", endDate="12/31/2020")
    writeJSONToFile('fundamentals_info', fundamentals_info)

except Exception as e:
    print(e)
    traceback.print_exc()
