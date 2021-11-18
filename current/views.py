import json
import os
from pprint import pprint
from django.shortcuts import render
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import tweepy

# index page with current top tweets, newsheadlines, crypto currency stocks
def index(request):
    """
    main view for displaying current data: cryptocurrency stocks and tweets
    """

    # initialize coinmarketcap API access and get crypto currency names for search_tweet 'q' parameter
    CRYPTO_URL = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    COINMARKETCAP_API_KEY = os.environ['COINMARKETCAP_KEY']
    currency_names = []
    parameters = {
        'start': '1',
        'limit': '10',
        'convert': 'CAD',
    }

    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
    }

    session = Session()
    session.headers.update(headers)
    currency_price_dict = {}

    try:
        response = session.get(CRYPTO_URL, params=parameters)
        data = json.loads(response.text)
        for entry in data['data']:
            currency_names.append(entry['name'])
            currency_price_dict[entry['name']] = {'CAD_price': entry['quote']['CAD']['price']}  
    except(ConnectionError, Timeout, TooManyRedirects) as e:
        pprint(e)
    
    # initialize twitter keys and tokens
    CONSUMER_KEY = os.environ['TWITTER_CONSUMER_KEY']
    CONSUMER_SECRET = os.environ['TWITTER_CONSUMER_SECRET']
    ACCESS_TOKEN = os.environ['TWITTER_ACCESS_TOKEN']
    ACCESS_SECRET = os.environ['TWITTER_ACCESS_SECRET']
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET )
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    # run search query with cryptocurrency names to get the top 5 tweets for both
    for name in currency_names:
        tweet_ids = []
        popular_tweets = api.search_tweets(q=name, result_type='popular', tweet_mode='extended', count=5)
        # get tweet id for embedding tweet in template
        for tweet_data in popular_tweets:
            if tweet_data._json['id']:
                tweet_ids.append(tweet_data._json['id'])
        # add tweet_ids to appropriate key in the currency_price_dict 
        if name in currency_price_dict.keys():
            currency_price_dict[name]['tweet_ids'] = tweet_ids

    context = {
        'currency_price_dict': currency_price_dict,

    }

    pprint(currency_price_dict)

    return render(request, 'current/index.html')