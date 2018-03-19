from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib

try:
    # For Python 3.0 and later
    from urllib.error import HTTPError
    from urllib.parse import quote
    from urllib.parse import urlencode
except ImportError:
    # Fall back to Python 2's urllib2 and urllib
    from urllib2 import HTTPError
    from urllib import quote
    from urllib import urlencode



# BEGIN YELP FUNCTIONS

# modified code found on git.hub https://github.com/Yelp/yelp-fusion/blob/master/fusion/python/sample.py

def request(host, path, api_key, url_params=None):
    url_params = url_params or {}
    url = '{0}{1}'.format(host, quote(path.encode('utf8')))
    headers = {
        'Authorization': 'Bearer %s' % api_key,
    }

  #  print(u'Querying {0} ...'.format(url))

    response = requests.request('GET', url, headers=headers, params=url_params)

    return response.json()


def search(api_key, term, location):
    url_params = {
        'term': term.replace(' ', '+'),
        'location': location.replace(' ', '+'),
        'limit': SEARCH_LIMIT
    }
    return request(API_HOST, SEARCH_PATH, api_key, url_params=url_params)


def get_business(api_key, business_id):
    business_path = BUSINESS_PATH + business_id

    return request(API_HOST, business_path, api_key)


def query_api(term, location):
    response = search(API_KEY, term, location)

    businesses = response.get('businesses')

    if not businesses:
        print(u'No businesses for {0} in {1} found.'.format(term, location))
        return

    business_id = businesses[0]['id']

    # print(u'{0} businesses found, querying business info ' \
    #     'for the top result "{1}" ...'.format(
    #         len(businesses), business_id))
    response = get_business(API_KEY, business_id)

  #  print(u'Result for business "{0}" found:'.format(business_id))
   # pprint.pprint(response, indent=2)
  
    print("Businesses:\n")
    
    x = 1
    for business in businesses:
        print(x)
        x += 1
        print(business['name'])
        print(business['location']['address1'])
        print(business['location']['city'] + ' ' + business['location']['state'] + ' ' + str(business['location']['zip_code']))
        print(" ")
        
# END YELP FUNCTIONS        

    
# BEGIN GoogleMaps FUNCTIONS 
def googleMaps(origin, destination):
    rawData = "https://maps.googleapis.com/maps/api/directions/json?origin="
    origin = origin.replace(" ", "_")
    destination = destination.replace(" ", "_")
    url = rawData + origin + (str("&destination=")) + destination + (str("&key=AIzaSyCdKiwSvdvdX_8xY1Ck9Kd5Qs5CPRf9VK0"))
    google = requests.get(url)
    data = google.json()
   
    data.keys()
    routes = data['routes']
    routes[0].keys()
    routes[0]['legs']
   
    legs = routes[0]['legs']
   
    miles = legs[0]['distance']['text']
    
    print ("\nYou are " + miles + " from " + CURRENT_CT + ".")
    
    time = legs[0]['duration']['text']
   
    print ("The drive will take " + time + " to get to " + CURRENT_CT + ".\n")        




#END GoogleMaps FUNCTIONS







#BEGIN Wunderground FUNCTIONS

import urllib2
import json

def wundergroundTempF(st, ct):

    rawData = "http://api.wunderground.com/api/30cc4655da9edc77/conditions/q/"

    state = st
    
    city = ct
    
    city = city.replace(" ", "_")

    url = rawData + state + str("/") + city + ".json"

    f = urllib2.urlopen(url)
    json_string = f.read()
    parsed_json = json.loads(json_string)
    temp_f = parsed_json['current_observation']['temperature_string']

    print ("The temperature in " + (ct) + " is currently " + (str(temp_f)))
    print (" ")
    

    f.close()

def wundergroundFunction():
    
    wundergroundTempF(CURRENT_ST,CURRENT_CT)
    
    parser = argparse.ArgumentParser()

    parser.add_argument('-q', '--term', dest='term', default=DEFAULT_TERM,
                        type=str, help='Search term (default: %(default)s)')
    parser.add_argument('-l', '--location', dest='location',
                        default=DEFAULT_LOCATION, type=str,
                        help='Search location (default: %(default)s)')

    input_values = parser.parse_args()

    try:
        query_api(input_values.term, input_values.location)
    except HTTPError as error:
        sys.exit(
            'Encountered HTTP error {0} on {1}:\n {2}\nAbort program.'.format(
                error.code,
                error.url,
                error.read(),
            )
        )

# END Wunderground FUNCTIONS 



        
        
        
        
#BEGIN MAIN FUNCTIONALITY

print("===========================")
print(" ")
print("Welcome to CityPocket!")
print("Please press enter after answering each question!")
print(" ")
print("===========================")
print(" ")



#yelp api constants 

API_KEY = 'nDXR-5q6Yi2KjT_W7QLWYz4KbfTLQYY4dhyX9Y2-Voau6hZugUlJEq12TdTOiBkJV1yGlhs4WF1i_wWfIuD1rWz5j5B7bxbZUegMQUkYbQwsph7AppDDWGFvDUOaWnYx'
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  

choice = ""

while choice.lower() != "no":
    # actual search criteria used to interface with our apis
    
    CURRENT_CT = raw_input("What city do you want to go to?\n> ")
    CURRENT_ST = raw_input("\nWhat state is it in?\n(format: 2 letters only)\n(ex: CA)\n> ")
    DEFAULT_LOCATION = CURRENT_CT + ", " + CURRENT_ST
    DEFAULT_TERM = raw_input("\nWhat do you want to search for in " + CURRENT_CT + "?\n> ")
    SEARCH_LIMIT = 3
    
    print (" ")
    
    
    
    if __name__ == '__main__':
        wundergroundFunction()
        
    TRAVEL = raw_input("\nWant to plan a trip to " + CURRENT_CT + "? (Please type Yes or No)\n>  ")
    print (" ")
    
    if TRAVEL.lower() == 'yes':
        origin = raw_input("\nWhat city are you in right now?\n> ")
        
        googleMaps(origin,CURRENT_CT)
        
    choice = raw_input("Do you want to plan a trip to another city? (Yes or No)\n> ") 
            
    
print(" ")
print("Happy Travels!")
print(" ")