import json
import os
from pprint import pprint
from django.shortcuts import render
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import tweepy

# index page with current crypto currency stocks, and popular tweets about them
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
        'limit': '5',
        'convert': 'CAD',
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY,
    }
    session = Session()
    session.headers.update(headers)
    crypto_price_dict = {}

    try:
        response = session.get(CRYPTO_URL, params=parameters)
        data = json.loads(response.text)
        for entry in data['data']:
            currency_names.append(entry['name'])
            crypto_price_dict[entry['name']] = entry['quote']['CAD']['price']
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

    # # run search queries with cryptocurrency names to get their embedded html code 
    # crypto_tweet_id_dict = {}
    # for name in currency_names:
    #     popular_tweets = api.search_tweets(q=name, result_type='popular', tweet_mode='extended', count=1)
    #     # get tweet id for embedding tweet in template
    #     for tweet_data in popular_tweets:
    #         pprint(tweet_data._json)
    #         if tweet_data._json['id']:
    #             url_to_embed = 'https://twitter.com/twitter/statuses/' + tweet_data._json['id_str']
    #             oembed_tweet_url = api.get_oembed(url=url_to_embed)
    #             crypto_tweet_id_dict[name] = oembed_tweet_url['html']

    context = {
        'crypto_price_dict': crypto_price_dict,
        # 'crypto_tweet_id_dict': crypto_tweet_id_dict,
    }

    pprint(crypto_price_dict)
    # pprint(crypto_tweet_id_dict)

    return render(request, 'current/index.html', context)