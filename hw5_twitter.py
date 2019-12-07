import sys
sys.path.append("/Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages") #this is to fix my own computer path directory error
import re

from requests_oauthlib import OAuth1
import json
import sys
import requests
import secret_data # file that contains OAuth credentials
# Uncomment following two lines after you install nltk
import nltk 
from nltk.corpus import stopwords

## SI 507 - HW5
## COMMENT WITH:
## Your section day/time: 003 Wednesday 10:00am
## Any names of people you worked with on this assignment:

#usage should be python3 hw5_twitter.py <username> <num_tweets>
username = sys.argv[1]
num_tweets = sys.argv[2]

consumer_key = secret_data.CONSUMER_KEY
consumer_secret = secret_data.CONSUMER_SECRET
access_token = secret_data.ACCESS_KEY
access_secret = secret_data.ACCESS_SECRET

#Code for OAuth starts
url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
auth = OAuth1(consumer_key, consumer_secret, access_token, access_secret)
requests.get(url, auth=auth)
#Code for OAuth ends

#Write your code below:

#Code for Part 3:Caching
CACHE_FNAME = 'tweet.json'

try: 
    cache_file = open(CACHE_FNAME, 'r')
    cache_content = cache_file.read()
    CACHE_DICTION = json.loads(cache_content)
    cache_file.close()
except: 
    CACHE_DICTION={}

#helper function to create the unique url combo for cache entry
def params_unique_combination(baseurl, params):
    alphabetized_keys = sorted(params.keys())
    res = []
    for k in alphabetized_keys:
        res.append("{}-{}".format(k, params[k]))
    return baseurl + "_" + "_".join(res)


# The main cache function
def make_request_using_cache(baseurl, params, auth):
    unique_ident = params_unique_combination(baseurl,params)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        print("Making a request for new data...")
        # Make the request and cache the new data
        resp = requests.get(baseurl, params,auth = auth)
        CACHE_DICTION[unique_ident] = json.loads(resp.text)
        dumped_json_cache = json.dumps(CACHE_DICTION,indent =4,ensure_ascii=False,)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]

#Code for Part 1:Get Tweets

def get_tweets(userid, tweetcount):
    baseurl = 'https://api.twitter.com/1.1/statuses/user_timeline.json'
    params = {'screen_name':username, 'count':int(num_tweets)}
    return make_request_using_cache(baseurl,params, auth)

#Code for Part 2:Analyze Tweets

response_list = get_tweets(username,num_tweets)
# create the tokens
tokens = []
for entry in response_list: 
    tokens+=nltk.word_tokenize(entry['text'])
# print(tokens)

#reference code: https://stackoverflow.com/questions/45138122/how-to-check-if-words-starts-with-within-the-alphabet-range
# https://stackoverflow.com/questions/2395821/python-startswith-any-alpha-character 
# only take tokens starting with a-zA-Z with regex
tokens_alphabet = [s for s in tokens if re.match('^[a-zA-Z]+.*', s)]

# https://www.geeksforgeeks.org/removing-stop-words-nltk-python/
# remove stopwords from the list

ignore_words = ['http','https','RT']
stop_words = set(stopwords.words('english'))
tokens_clean = []
for word in tokens_alphabet:
    if word not in ignore_words:
        if word not in stop_words:
            tokens_clean.append(word)

token_dict = {}
for token in tokens_clean: 
    if token in token_dict:
        token_dict[token] += 1
    else: 
        token_dict[token] = 1

sorted_token_dict = sorted(token_dict.items(),key = lambda x: x[1],reverse = True)
for i in range(5):
    print(sorted_token_dict[i][0])

if __name__ == "__main__":
    if not consumer_key or not consumer_secret:
        print("You need to fill in client_key and client_secret in the secret_data.py file.")
        exit()
    if not access_token or not access_secret:
        print("You need to fill in this API's specific OAuth URLs in this file.")
        exit()
