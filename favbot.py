# coding=utf-8

import ConfigParser
import time
import twitter
from random import choice

searches = [
    #u"snap",
    u"@cah",
    u'"cards against humanity"',
    u'"apples to apples"'
]

def setup_api():
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
    return api


def update_self_favorites_list_and_find_tweet_to_favorite(api):
    my_favs = api.GetFavorites()
    print my_favs
    faved_users = ["CAH"]
    # key by id to make checking for fav'd tweets easy
    for faved in my_favs:
        faved_users.append(faved.user.screen_name)
    print "Already faved users: %s" % faved_users
    print "Finding tweet to fav now"
    rando_search = "%s -'RT'" % choice(searches)
    print "Searching for '%s'" % rando_search
    search_results = api.GetSearch(rando_search)
    #print search_results
    status = choice(search_results)
    #print "Status id to check: %s" % status.id
    if status.user.screen_name not in faved_users:
        if not status.GetInReplyToScreenName() and not "snap" in status.user.screen_name.lower() and not status.text[0] == "@":
            # it's probably ok to fav more than once, the request
            # will just fail
            try:
                api.CreateFavorite(status)
                print "Favorited tweet: %s from %s" % (status.id, status.user.screen_name)
                print status.text
                print "-----"

            except twitter.TwitterError as e:
                # if we already fav'd just ignore and go to next
                if "favorite per day" in e.message:
                    print "Rate limited by Twitter, waiting a while before we try again."
                    time.sleep(60 * 60)
                else:
                    print "Already favorited tweet %s or some other error"  % status.id
                    print "Error is: %s" % e.message
                pass
            except:
                raise
        else:
            print "%s - %s" % (status.user.screen_name, status.text)
            print "Has Snap in screen name, or is reply... trying again..."
    else:
        print "Already faved user %s, trying again..." % status.user.screen_name


if __name__ == "__main__":
    print "Starting up!"
    api = setup_api()
    # run forever!
    while(True):
        update_self_favorites_list_and_find_tweet_to_favorite(api)
        time.sleep(30)



