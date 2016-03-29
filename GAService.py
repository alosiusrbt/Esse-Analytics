"""A simple example of how to access the Google Analytics API."""

import argparse

from googleapiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

import httplib2
from oauth2client import client
from oauth2client import file
from oauth2client import tools
import pprint
from urllib2 import HTTPError


# START: Logger 

import time
import logging
import datetime
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# create a file handler
handler = logging.FileHandler('F:\Dev_Sample_Projects\google-flask\Access_log_'+datetime.datetime.now().strftime("%Y-%m-%d")+'.log')
handler.setLevel(logging.INFO)
# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(handler)
# END: Logger 

# START: Config Section
try:
  from settings import h2oPyConfig
except Exception as err:
  logger.info('Exception: '+str(err))
settings = h2oPyConfig.cfg['google_analytics']

def get_service(api_name, api_version, scope, key_file_location,
                service_account_email):
  """Get a service that communicates to a Google API.

  Args:
    api_name: The name of the api to connect to.
    api_version: The api version to connect to.
    scope: A list auth scopes to authorize for the application.
    key_file_location: The path to a valid service account p12 key file.
    service_account_email: The service account email address.

  Returns:
    A service that is connected to the specified API.
  """
  logger.info('started reading key_file_location')
  f = open(key_file_location, 'rb')
  key = f.read()
  f.close()
  logger.info('key_file_location read')
  logger.info('Google API Authenticatetion STARTED')
  credentials = SignedJwtAssertionCredentials(service_account_email, key,
    scope=scope)
  logger.info('Got credentials')
  http = credentials.authorize(httplib2.Http())
  logger.info('Authenticatetion FINISHED')
  # Build the service object.
  logger.info('Service object build started')
  service = build(api_name, api_version, http=http)
  logger.info('Service object built')
  
  return service

def get_profile_array(service):
  try:
    accounts = service.management().accounts().list().execute()
    profile_collection = []
    for acc in accounts.get("items"):
      properties = service.management().webproperties().list(accountId=acc["id"]).execute()
      for prop in properties.get("items"):
        profiles = service.management().profiles().list(accountId=acc["id"], webPropertyId=prop["id"]).execute()
        for prof in profiles.get("items"):
          profile_collection.append(prof["id"])
    return profile_collection
  except TypeError, error:
    # Handle errors in constructing a query.
    logger.info('There was an error in constructing your query : %s' % error)

  except HTTPError, error:
    # Handle API errors.
    logger.info('There was an API error : %s : %s' %
           (error.resp.status, error.resp.reason))


def get_first_profile_id(service):
  # Use the Analytics service object to get the first profile id.

  # Get a list of all Google Analytics accounts for this user
  accounts = service.management().accounts().list().execute()

  if accounts.get('items'):
    # Get the first Google Analytics account.
    account = accounts.get('items')[0].get('id')

    # Get a list of all the properties for the first account.
    properties = service.management().webproperties().list(
        accountId=account).execute()

    if properties.get('items'):
      # Get the first property id.
      property = properties.get('items')[0].get('id')

      # Get a list of all views (profiles) for the first property.
      profiles = service.management().profiles().list(
          accountId=account,
          webPropertyId=property).execute()

      if profiles.get('items'):
        # return the first view (profile) id.

        return profiles.get('items')[0].get('id')

  return None



def get_accounts_ids(service):
    accounts = service.management().accounts().list().execute()
    ids = []
    if accounts.get('items'):
        for account in accounts['items']:
            ids.append(account['id'])
   
    return ids

def getPageViews(service, profile_id,start_date='yesterday',end_date='today'):
  # Use the Analytics Service Object to query the Core Reporting API
  # for the number of sessions within the past seven days.
  logger.info(start_date)
  logger.info(end_date)
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=start_date,
      end_date=end_date,
      dimensions='ga:pagepath',
      metrics='ga:users,ga:pageviews').execute()


def fix_unicode(data):
    if isinstance(data, unicode):
        return data.encode('utf-8')
    elif isinstance(data, dict):
        data = dict((fix_unicode(k), fix_unicode(data[k])) for k in data)
    elif isinstance(data, list):
        for i in xrange(0, len(data)):
            data[i] = fix_unicode(data[i])
    return data


def getRows(results):
  # Print data nicely for the user.
  if results:
    logger.info('View (Profile): %s' % results.get('profileInfo').get('profileName'))
    logger.info('Total Sessions: %s' % results.get('rows')[0][0])
    logger.info(results);
    unicodedata = results.get('rows')
    for singleArray in unicodedata:
        stringdata = fix_unicode(unicodedata)

    
    
    return stringdata
    
def getCols(results):
  if results:
    logger.info('View (Profile): %s' % results.get('profileInfo').get('profileName'))
    logger.info('Total Sessions: %s' % results.get('rows')[0][0])
    logger.info("''''''''''''''''''''''''")
    try:
      logger.info(results.get('columnHeaders'))
      unicodedata = results.get('columnHeaders')
      for singleArray in unicodedata:
          stringdata = fix_unicode(unicodedata)
      columns = []
      for t in stringdata:
        columns.append(t["name"].split("ga:")[1])
      return columns
    except Exception as e:
      logger.info("''''''''''Custom error message''''''''''")
      logger.info(e) 
# for n in conn.notices():
#   pprint(n)
  else:
    logger.info('No results found')

def googleAuthenticate():
    # Define the auth scopes to request.
    scope = ['https://www.googleapis.com/auth/analytics.readonly']

    # Use the developer console and replace the values with your
    # service account email and relative location of your key file.
    service_account_email = settings['service_account_email']
    key_file_location = settings['key_file_location']

    # Authenticate and construct service.
    logger.info('------START: Authentication--------')
    service = get_service('analytics', 'v3', scope, key_file_location,
      service_account_email)
    logger.info(service)
    logger.info('------END: Service--------')
    return service

def getAllControllerPageViews(service, profile_id):
  try:
    logger.info('------START: Print Results--------')
    
    results = getPageViews(service, profile_id, start_date="2016-02-01")
    if "rows" in results:
      logger.info(getRows(results))
      logger.info(getCols(results))
    logger.info('------END: Print Results--------')
    return results
  except Exception as err:
    logger.info('Exception: '+str(err))

def getData(service, profiles):
  result = []
  for obj in profiles:
    result.append(getAllControllerPageViews(service, obj))
  return result

def getColumnChartAllControllerPageViews(service, profiles):
  try:
    if not service:
      service = googleAuthenticate()
    from Helpers.ChartDataConstructor import ChartDataConstructor
    result = getData(service, profiles)
    cls = ChartDataConstructor()
    response = cls.getColumnChart(getCols(result[0]),result)
    return_data = dict()
    return_data["consolidatedResult_Columns"] = response[0:1]
    return_data["consolidatedResult_Data"] = response[1:len(response)] 
    return return_data
  except Exception as e:
    logger.info(":::::::::::::::::::::::::::::::::::::::::::::")
    logger.info(e)

def getAllSessionData(service, profiles):
  result = []
  for obj in profiles:
    result.append(executeSessionData(service, obj, '2016-02-01'))
  return result

def executeSessionData(service,profile_id,start_date='yesterday',end_date='today'):
    # Use the Analytics Service Object to query the Core Reporting API
  # for the number of sessions within the past seven days.
  logger.info(start_date)
  logger.info(end_date)
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=start_date,
      end_date=end_date,
      dimensions='',
      metrics='ga:users,ga:sessions,ga:percentNewSessions').execute()

def executeAvgSessionData(service,profile_id,start_date='yesterday',end_date='today'):
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=start_date,
      end_date=end_date,
      dimensions='',
      metrics='ga:sessions,ga:sessionDuration,ga:avgSessionDuration').execute()

def executeTimePerPage(service,profile_id,start_date='yesterday',end_date='today'):
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date=start_date,
      end_date=end_date,
      dimensions='ga:pagePath',
      metrics='ga:timeOnPage,ga:avgTimeOnPage').execute()

def getColumChartSeparateControllerPageViews(service, profiles):
  try:
    if not service:
      service = googleAuthenticate()
    from Helpers.ChartDataConstructor import ChartDataConstructor
    import json
    cls = ChartDataConstructor()
    result = getData(service, profiles)
    return_data = dict()
    return_data["separateData"] = cls.getSeparateColumnChartData(getCols(result[0]),result) 
    return return_data
  except Exception as e:
    logger.info("++++++++++++++++++++++++++++++++++++++++++==")
    logger.info(e)  

def getDashboardDetails(service, profiles):
  try:
    if not service:
      service = googleAuthenticate()
    from Helpers.ChartDataConstructor import ChartDataConstructor
    import json
    result = getAllSessionData(service, profiles)
    t = [0,0,0]
    for obj in result:
      if "rows" in obj:
        t = [float(x) + float(y) for x, y in zip(t, obj["rows"][0])]
    t[2] = t[2] / len(result)
    return_data = dict()
    return_data["controllers"] = len(profiles)
    return_data["sessionCount"] = t[1]
    return_data["percentNewSessions"] = t[2]
    return return_data
  except Exception as e:
    logger.info("=========================================")
    logger.info(e)

def getAverageSession(service, profiles):
  try:
    result = []
    from Helpers.DateTimeParser import DateTimeParser
    for obj in profiles:
      queryResult = executeAvgSessionData(service, obj, '2016-02-01')
      sessDict = dict()
      sessDict["profileName"] = queryResult["profileInfo"]["profileName"]
      sessDict["sessions"] = queryResult["totalsForAllResults"]["ga:sessions"]
      sessDict["sessionDuration"] = DateTimeParser.format_seconds_to_hhmmss(queryResult["totalsForAllResults"]["ga:sessionDuration"])
      sessDict["avgSessionDuration"] = DateTimeParser.format_seconds_to_hhmmss(queryResult["totalsForAllResults"]["ga:avgSessionDuration"])
      result.append(sessDict)
    return result
  except Exception as e:
    logger.info(e)    

def getTimePerPage(service, profiles):
  try:
    results = []
    for obj in profiles:
      result = executeTimePerPage(service,obj,'2016-02-01')
      if "rows" in result:
        logger.info(getRows(result))
        logger.info(getCols(result))
        logger.info('------END: Print Results--------')
        results.append(result)
    return results
  except Exception as e:
    logger.info("'''''''''getTimePerPage''''''''''")
    logger.info(e)

def getTimePerPageForAllControllers(service, profiles):
  result = getTimePerPage(service, profiles)
  from Helpers.ChartDataConstructor import ChartDataConstructor
  from Helpers.DateTimeParser import DateTimeParser
  cls = ChartDataConstructor()
  response = cls.getColumnChart(getCols(result[0]),result)
  return_data = dict()
  return_data["colHeader"] = response[0:1]
  return_data["data"] = response[1:len(response)] 
  # for obj in return_data["data"]:
  #   obj[1] = DateTimeParser.format_seconds_to_hhmmss(obj[1])
  #   obj[2] = DateTimeParser.format_seconds_to_hhmmss(obj[2])
  return return_data

def getSessionDashboardDetails(service, profiles):
  try:
    if not service:
      service = googleAuthenticate()
    resultSet = dict()
    resultSet["AvgSession"] = getAverageSession(service, profiles)
    return resultSet
  except Exception as e:
    logger.info("--------------Exception : getSessionDashboardDetails-----------------")
    logger.info(e)
