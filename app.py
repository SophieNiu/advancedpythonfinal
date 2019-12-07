from __future__ import print_function

import argparse
import json
import pprint
import requests
import sys
import urllib
import secrets

# This client code can run on Python 2.x or 3.x.  Your imports can be
# simpler if you only need one of those.
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

API_KEY = secrets.api_key
# No long need clientid

# ref: https://github.com/Yelp/yelp-fusion/blob/master/fusion/python/sample.py

# API constants, you shouldn't have to change these.
API_HOST = 'https://api.yelp.com'
SEARCH_PATH = '/v3/businesses/search'
BUSINESS_PATH = '/v3/businesses/'  # Business ID will come after slash.

# Create cache file
CACHE_FNAME = 'yelp.json'

try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_content = cache_file.read()
    CACHE_DICTION = json.loads(cache_content)
    cache_file.close()
except:
    CACHE_DICTION = {}

# helper function to create the unique url combo for cache entry


def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_" + "_".join(res)


# The main cache function
def make_request_using_cache(baseurl, params, auth):
    unique_ident = params_unique_combination(baseurl, params)

    # first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    # if not, fetch the data afresh, add it to the cache,
    # then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params, auth=auth)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(
            CACHE_DICTION, indent=4, ensure_ascii=False,)
        fw = open(CACHE_FNAME, "w")
        fw.write(dumped_json_cache)
        fw.close()  # Close the open file
        return CACHE_DICTION[unique_ident]


def get_busi():

    headers = {
        'Authorization': 'Bearer %s' % API_KEY,
    }

    url_params = {
        'categories': 'bars',
        'location': 'New York City',
        'limit': 50,
    }

    response = requests.request(
        'GET', API_HOST+SEARCH_PATH, headers=headers, params=url_params)


print(type(response))
