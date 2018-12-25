@auth.requires_login()
def get_keyword():
    '''
    >>> i=get_keyword();i["Other Message"]
    '''
    otherMessage="Message"

    form=SQLFORM(db.t_keyword_table)

    if form.process().accepted:
        myrows=db(db.t_keyword_table.created_by==session.auth.user.id).select(db.t_keyword_table.ALL,orderby=db.t_keyword_table.id)
        last_row=myrows.last()
        if (last_row.f_marketing_aim1 == "" or last_row.f_marketing_aim2 == "" or last_row.f_search_key1 == "" or last_row.f_search_key2 == "" or last_row.f_search_key3 == "" or last_row.f_weight_1 == "" or last_row.f_weight_2 == "" or last_row.f_weight_3 == "" or last_row.f_tweet_count == ""):
            redirect(URL('warning','check_keywordtable'))
        else:
            tweetlimit = last_row.f_tweet_count
            weight1=last_row.f_weight_1
            weight2=last_row.f_weight_2
            weight3=last_row.f_weight_3
            weight_sum = (weight1+weight2+weight3)
            if (tweetlimit<121 and weight_sum==100):
                get_tweet()
                redirect(URL('datacollection','analyse_tweetnew'))
            else:
                if tweetlimit>50000:
                    redirect(URL('warning','check_keywordtable'))
                elif weight_sum != 100:
                    redirect(URL('warning','check_keywordtable'))
                else:
                    redirect(URL('warning','wait_time'))
    elif form.errors:
        response.flash = 'Form has errors'
    else:
        response.flash = 'Please fill out the form'
        return dict(form=form, otherMessage=otherMessage)


@auth.requires_login()
def get_tweet():
    #Get the latest searched key
    myrows=db(db.t_keyword_table.created_by==session.auth.user.id).select(db.t_keyword_table.ALL,orderby=db.t_keyword_table.id)
    last_row=myrows.last()
    aim1 = last_row.f_marketing_aim1
    aim2 = last_row.f_marketing_aim2
    key1 = last_row.f_search_key1
    key2 = last_row.f_search_key2
    key3 = last_row.f_search_key3
    tweetlimit = last_row.f_tweet_count

    import tweepy
    from tweepy import Stream
    from tweepy import OAuthHandler
    from tweepy.auth import OAuthHandler
    from tweepy.streaming import StreamListener
    import time

    #############################################################################
    #User credentials to access Twitter API
    #############################################################################

    access_token = "1697250469-DlD70jh0hW7hhDsYuxDUJcakl9shT1ZY44nSqea"
    access_token_secret = "hRPzpjqZZe0KgyPQZRPTlQM2DvIDH8L6DFfwpwojCn5dK"
    consumer_key = "avZpwnKrmiSwjOd0SPxAUAuO5" #API Key
    consumer_secret = "SCGrIaNkGRrYGXQ2HMiDsgQLqV6pfBgFA0RCjxr2b20Om3D4OC" #API Secret Key

    #This handles Twitter authentification and the connection to Twitter Streaming API
    #auth = tweepy.OAuthHandler('avZpwnKrmiSwjOd0SPxAUAuO5', 'SCGrIaNkGRrYGXQ2HMiDsgQLqV6pfBgFA0RCjxr2b20Om3D4OC')
    #auth.set_access_token('1697250469-DlD70jh0hW7hhDsYuxDUJcakl9shT1ZY44nSqea', 'hRPzpjqZZe0KgyPQZRPTlQM2DvIDH8L6DFfwpwojCn5dK')
    #api=tweepy.API(auth)

    class TwitterStreamListener(tweepy.StreamListener):
        def __init__(self):
            super(TwitterStreamListener, self).__init__()
            self.counter = 0
            self.limit = tweetlimit



        def on_status(self, status):
            try:
                db.tweets.insert(search_id=last_row.id,tweet_id=status.id, username=status.author.screen_name, tweet_text=status.text,tweet_language=status.lang, followers=status.author.followers_count, country=status.author.location,tweet_retweets=status.retweet_count, tweet_creationdate=status.created_at,tweet_source=status.source,retweeted=status.retweeted,tweet_favoritecount=status.favorite_count,usersince=status.author.created_at,user_geoenabled=status.author.geo_enabled, coordinate=status.coordinates)
                db.commit()
                self.counter += 1
                aim1_count=db(db.tweets.tweet_text.contains(aim1)).count()
                aim2_count=db(db.tweets.tweet_text.contains(aim2)).count()
                keyword1_count=db(db.tweets.tweet_text.contains(key1)).count()
                keyword2_count=db(db.tweets.tweet_text.contains(key2)).count()
                keyword3_count=db(db.tweets.tweet_text.contains(key3)).count()
                if (aim1_count+aim2_count+keyword1_count+keyword2_count+keyword3_count) < self.limit:
                    return True
                else:
                    twitterStream.disconnect()
            except BaseException as e:
                time.sleep(5)

        def on_error(self, status_code):
            if status_code == 420:# Rate limit reached
                return False # disconnects stream


    autho = tweepy.OAuthHandler('avZpwnKrmiSwjOd0SPxAUAuO5', 'SCGrIaNkGRrYGXQ2HMiDsgQLqV6pfBgFA0RCjxr2b20Om3D4OC')
    autho.secure = True
    autho.set_access_token('1697250469-DlD70jh0hW7hhDsYuxDUJcakl9shT1ZY44nSqea', 'hRPzpjqZZe0KgyPQZRPTlQM2DvIDH8L6DFfwpwojCn5dK')
    api=tweepy.API(autho, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)
    streamListener = TwitterStreamListener()
    twitterStream = tweepy.Stream(auth = api.auth, listener=streamListener)
    twitterStream.filter(languages=["en"], track=[aim1,aim2,key1,key2,key3])

    return locals()


def analyse_tweetnew():
    grid = SQLFORM.grid(db[db.tweets])
    import pandas as pd
    import matplotlib.pyplot as plt
    import plotly.offline as py
    import plotly.graph_objs as go

    myrows=db(db.t_keyword_table.created_by==session.auth.user.id).select(db.t_keyword_table.ALL,orderby=db.t_keyword_table.id)
    last_row=myrows.last()
    aim1 = last_row.f_marketing_aim1
    aim2 = last_row.f_marketing_aim2
    key1 = last_row.f_search_key1
    key2 = last_row.f_search_key2
    key3 = last_row.f_search_key3
    tweetlimit = last_row.f_tweet_count

    language_count=db(db.tweets.tweet_language=='en').count()
    aim1_count=db(db.tweets.tweet_text.contains(aim1)).count()
    aim2_count=db(db.tweets.tweet_text.contains(aim2)).count()
    aim1_key1_count=db(db.tweets.tweet_text.contains([aim1,key1],all=True)).count()
    aim1_key2_count=db(db.tweets.tweet_text.contains([aim1,key2],all=True)).count()
    aim1_key3_count=db(db.tweets.tweet_text.contains([aim1,key3],all=True)).count()
    aim2_key1_count=db(db.tweets.tweet_text.contains([aim2,key1],all=True)).count()
    aim2_key2_count=db(db.tweets.tweet_text.contains([aim2,key2],all=True)).count()
    aim2_key3_count=db(db.tweets.tweet_text.contains([aim2,key3],all=True)).count()

    keyword1_count=db(db.tweets.tweet_text.contains(key1)).count()
    keyword2_count=db(db.tweets.tweet_text.contains(key2)).count()
    keyword3_count=db(db.tweets.tweet_text.contains(key3)).count()


    return locals()
