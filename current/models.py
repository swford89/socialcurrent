from django.db import models

class News(models.Model):
    headline = models.CharField(max_length=250)
    publication_date = models.DateTimeField()


class Tweet(models.Model):
    created_at = models.DateTimeField()                 # date of the tweet
    favorite_count = models.IntegerField()              # measure of popularity
    full_text = models.TextField()
    tweet_id = models.IntegerField()
    user_name = models.CharField(max_length=100)        # user who tweeted tweet
    verified_user = models.BooleanField()               # make sure user is verified
    tweet_url = models.URLField()                       # https://twitter.com/twitter/statuses/ + (tweet id number)


class CryptoCurrency(models.Model):
    cmc_rank = models.IntegerField()                    # CoinMarketCap Ranking
    date_added = models.DateTimeField()
    crypto_name = models.CharField(max_length=100)
    circulating_supply = models.BigIntegerField()       # Currency amount in circulation
    latest_update = models.DateTimeField()              # Date and time of current stats
    percent_change_1hr = models.FloatField()
    percent_change_24hr = models.FloatField()
    percent_change_7d = models.FloatField()
    percent_change_30d = models.FloatField()
    
