# Script for pulling data from the GFD Series API

import requests
import pandas as pd
import datetime
import os
import json
from datetime import datetime
import traceback
# import matplotlib.pyplot as plt
# plt.close('all')

GFD_API_URL = "https://api.finaeon.com"
GFD_USERNAME = "tryapi@finaeon.com"
GFD_PASSWORD = "Test!123"

def writeJSONToFile(fileSuffix, jsonContents):
    now = datetime.now()
    jsonFilename = now.strftime("%Y%m%d-%H%M%S%f") + '_' + fileSuffix +'.json'
    relativeDirectory = './responses/'
    if not os.path.isdir(relativeDirectory):
        os.mkdir(relativeDirectory)
    outputfilepath = relativeDirectory + jsonFilename
    with open(outputfilepath,'w') as f:
        json.dump(jsonContents, f)

def call_api(path, parameters):
    url = GFD_API_URL + path
    headers = {'Content-type': 'application/json'}
    print("calling %s" % url)
    print("request body: \r\n %s" % parameters)
    writeJSONToFile(path.strip('/') + 'Request', parameters)
    resp = requests.post(url, headers=headers, data = json.dumps(parameters))
    return resp

def gfd_auth(username, password):
    parameters = {'username': username, 'password': password}
    resp = call_api('/login', parameters=parameters)

    #check for unsuccessful API returns
    if resp.status_code != 200:
        raise ValueError('GFD API request failed with HTTP status code %s' % resp.status_code)

    json_content = resp.json()
    print("GFD API token recieved at %s" % str(datetime.now()))
    return json_content

def gfd_search(token, searchString, **kwargs):
    page = kwargs.get('page',None)
    pageSize = kwargs.get('pageSize',None)
    searchType = kwargs.get('searchType',None)
    baseFilter = kwargs.get('baseFilter',None)
    sort = kwargs.get('sort',None)
    parameters = {'token': token,
                  "page": page,
                  "pageSize": pageSize,
                  "searchString": searchString,
                  "searchType": searchType,
                  "baseFilter": baseFilter,
                  "sort": sort
                  }
    parameters = {key:val for key, val in parameters.items() if val != None}
    r = call_api('/search', parameters=parameters)
    search_data = r.json() 
    return search_data

def gfd_searchbycikcodes(token, cikCodes):
    parameters = { "token": token, "cikCodes": cikCodes }
    parameters = {key:val for key, val in parameters.items() if val != None}
    r = call_api('/searchbycikcodes', parameters)
    searchbycikcodes_data = r.json() 
    return searchbycikcodes_data

def gfd_series(token, **kwargs):
    seriesId = kwargs.get('seriesId',None)
    seriesName = kwargs.get('seriesName',None)
    splitAdjusted = kwargs.get('splitAdjusted',None)
    startDate = kwargs.get('startDate',None)
    endDate = kwargs.get('endDate',None)
    periodicity = kwargs.get('periodicity',None)
    closeOnly = kwargs.get('closeOnly',None)
    currency = kwargs.get('currency',None)
    inflationAdjusted = kwargs.get('inflationAdjusted',None)
    annualFlow = kwargs.get('annualFlow',None)
    totalReturn = kwargs.get('totalReturn',None)
    corporateActions = kwargs.get('corporateActions',None)
    metadata = kwargs.get('metadata',None)
    incFields = kwargs.get('incFields',None)
    includeAverage = kwargs.get('includeAverage',None)
    periodPercentChange = kwargs.get('periodPercentChange',None)
    parameters = {'token': token,
                  "seriesId": seriesId,
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
                  "periodPercentChange": periodPercentChange
                  }

    parameters = {key:val for key, val in parameters.items() if val != None}
    r = call_api('/series', parameters=parameters)
    series_data = r.json() 
    return series_data

def gfd_fundamentals(token, seriesName, period, **kwargs):
    startDate = kwargs.get('startDate',None)
    endDate = kwargs.get('endDate',None)
    group = kwargs.get('group',None)
    parameters = {'token': token,
                  "seriesName": seriesName,
                  "period": period,
                  "startDate": startDate,
                  "endDate": endDate,
                  "group": group
                }
    parameters = {key:val for key, val in parameters.items() if val != None}
    r = call_api('/fundamentals', parameters)
    fundamentals_data = r.json() 
    return fundamentals_data


try:
    # Call the gfd_auth function with credentials
    authJSON = gfd_auth(GFD_USERNAME, GFD_PASSWORD)
    writeJSONToFile('Login', authJSON)

    # Store Token from json response
    token = authJSON['token'].strip('"')
    print("Token:\r\n%s\r\n" % token)

    series_price_data = gfd_series(token, seriesName="IBM", startDate="01/01/2017", closeOnly="true", periodicity="monthly")
    # series_price_data = gfd_series(token, 
    #                                seriesId="55970", 
    #                                splitAdjusted="true", 
    #                                startDate="01/01/2017", 
    #                                endDate="01/01/2020", 
    #                                periodicity="monthly", 
    #                                closeOnly="false", 
    #                                currency="USD", 
    #                                inflationAdjusted="false", 
    #                                annualFlow="false", 
    #                                totalReturn="false",
    #                                corporateActions="false",
    #                                metadata="true",
    #                             #    incFields="send,sbegin",
    #                                includeAverage="false",
    #                                periodPercentChange="false")
    writeJSONToFile('series_price_data', series_price_data)
    data = pd.DataFrame(series_price_data['price_data'])
    print(data)

    # pivot based on series
    # df_columns = data.pivot(index="date", columns="series_id", values="close")
    # print(df_columns)

    # ax = df_columns.plot()
    # ax.set_ylim(ymin=0)
    # plt.show()

    # search API call
    search_info = gfd_search(token, searchString="IBMY", searchType="symbol", baseFilter="startsWith")
    # search_info = gfd_search(token, searchString="General Motors", searchType="name", baseFilter="contains")
    # search_info = gfd_search(token, searchString="General Motors", searchType="name", baseFilter="contains", sort="pop", page="3", pageSize="10")
    writeJSONToFile('search_info', search_info)

    # search by cik API Call
    search_info_by_cik = gfd_searchbycikcodes(token, cikCodes="0000354950,0000789019")
    writeJSONToFile('search_info_by_cik', search_info_by_cik)

    #use dictionary comp to build a dict
    search_dict = {s["symbol"]:s for s in search_info["search_results"]}
    # print(search_dict)

    # print('keys', search_dict.keys())

    # get data by keys
    # looping through each key and building a new dictionary
    # data_dict = {k:gfd_series(token, seriesName=k, periodicity="monthly", totalReturn="true", startDate="01/01/2020", closeOnly="true") for k in search_dict.keys()}
    # print(data_dict)

    # fundementals_info = gfd_fundamentals(token, "MSFT", "Annual")
    fundementals_info = gfd_fundamentals(token, seriesName="MSFT", period="Annual", group="Balance Sheet", startDate="01/01/2010", endDate="12/31/2020")
    writeJSONToFile('fundementals_info', fundementals_info)

except Exception as e:
    print(e)
    traceback.print_exc()

