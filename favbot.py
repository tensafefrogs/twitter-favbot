# coding=utf-8

import ConfigParser
import time
import twitter

def startup():
    config = ConfigParser.ConfigParser()
    config.read('snapsnapgo-favbot.cfg')

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
        faved_ids[faved.id] = faved
    print "Finding tweet to fav now"
    search_results = api.GetSearch('snap -"RT"')
    print search_results
    for status in search_results:
        if status.id not in faved_ids:
            if not status.in_reply_to_user_id:
                # it's probably ok to fav more than once, the request
                # will just fail
                print "Favoriting tweet: %s from %s" % (status.id, status.user.screen_name)
                api.CreateFavorite(status.id)




if __name__ == "__main__":
    print "Starting up!"
    startup()

