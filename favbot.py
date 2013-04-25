# coding=utf-8

import ConfigParser
import time
import twitter

def startup():
    config = ConfigParser.ConfigParser()
    config.read('snapsnapgo-favbot.cfg')


    """
    Create your config file like so:
    [tokens]
    consumer_key = key
    consumer_secret = secret
    access_token_key = at_key
    access_token_secret = at_secret
    """
    api = twitter.Api( consumer_key=config.get('tokens','consumer_key'),
                  consumer_secret=config.get('tokens','consumer_secret'),
                  access_token_key=config.get('tokens','access_token_key'),
                  access_token_secret=config.get('tokens','access_token_secret')
          )
    try:
        print "Attempting to connect with the api..."
        print api.VerifyCredentials()
    except twitter.TwitterError:
        raise
    except:
        raise

    update_self_favorites_list_and_find_tweet_to_favorite(api)


def update_self_favorites_list_and_find_tweet_to_favorite(api):
    my_favs = api.GetFavorites()
    print my_favs
    faved_ids = []
    # key by id to make checking for fav'd tweets easy
    for faved in my_favs:
        faved_ids.append(faved.id)
    print "Already faved ids: %s" % faved_ids
    print "Finding tweet to fav now"
    search_results = api.GetSearch('snap -"RT"')
    #print search_results
    for status in search_results:
        #print "Status id to check: %s" % status.id
        if status.id not in faved_ids:
            if not status.GetInReplyToScreenName():
                # it's probably ok to fav more than once, the request
                # will just fail
                print "Favoriting tweet: %s from %s" % (status.id, status.user.screen_name)
                try:
                    api.CreateFavorite(status)
                    # wait a few seconds before continuing so we don't piss of twitter
                    time.sleep(10)

                    # do it all again!
                    update_self_favorites_list_and_find_tweet_to_favorite(api)
                except twitter.TwitterError:
                    # if we already fav'd just ignore and go to next
                    pass
                except:
                    raise




if __name__ == "__main__":
    print "Starting up!"
    startup()

