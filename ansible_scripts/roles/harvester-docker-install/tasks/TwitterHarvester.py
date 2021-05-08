import json
import couchdb
import tweepy
import time
from datetime import datetime

from tweepy import TweepError

token_list = [
{
        "ACCOUNT_NAME": "TD1",
        "ACCESS_TOKEN": "1382216257299095553-UFdedtyG9RMYPpJ5hrDi0bHaeBFsre",
        "ACCESS_TOKEN_SECRET": "aCTcoaD02YvgRBVHqvpupl51c26cpgB7MLqGNvjTdgYHY",
        "CONSUMER_KEY": "HzSYdI0t164WwtK6VI9WkVgn0",
        "CONSUMER_SECRET": "4RDA9ZUsl0soZwePswYrF1hKWmZQRKfeAnG2hbTlR5IpJC4v3y",
        "GEO": "37.8136,144.9631,300km",
        "GEO_NAME": "MELBOURNE"
    },
    {
        "ACCOUNT_NAME": "TD2",
        "ACCESS_TOKEN": "1388622253567344642-jVEgR0vfEfQtocxvqkjJivByxSEQYL",
        "ACCESS_TOKEN_SECRET": "tCh41arAjdH8rJhjdHNhNjg3WEDwsjG6fgWlCVokE8F1T",
        "CONSUMER_KEY": "j4HuqFwBjsHCaWLG53AGhaqed",
        "CONSUMER_SECRET": "L5P1rQB1QWwkaWAEig3hb3pVsfvyAwbSHGSWVD5EruWIoa5ivt",
        "GEO": "31.9523,115.8613,300km",
        "GEO_NAME": "PERTH"
    },
    {
        "ACCOUNT_NAME": "SM1",
        "ACCESS_TOKEN": "1385176748229160963-lAKIZyu6S4IWbGJ3PlWaj42Vib6KHl",
        "ACCESS_TOKEN_SECRET": "Uf3dPXCJ2eJE2MyHKX4qInSJJacQkFhz1pssESk5L4xfb",
        "CONSUMER_KEY": "1TWIf5dxovtRAgsewLnAMswVf",
        "CONSUMER_SECRET": "4Fqys3SJKUaXIs929qKxS6nLJI6hLkgmid5ugn1CrlrHuAtNQ2",
        "GEO": "34.9285,138.6007,300km",
        "GEO_NAME": "ADELAIDE"
    },
    {
        "ACCOUNT_NAME": "SM2",
        "ACCESS_TOKEN": "1037915277260804102-179ZUFODI6ShQDVLMZpMr3XlniHY2M",
        "ACCESS_TOKEN_SECRET": "CyrVLUzPDSEOlScOO6xzJfR7XYBJuBV3j1ksRDpljlJCa",
        "CONSUMER_KEY": "ZRTNsGfjmBKZk6UWKgKgLCuOp",
        "CONSUMER_SECRET": "AaFOLb2k5ZZLcV516Ht1cS8BeusN9B1GddFuMH82tc8t4YkAhP",
        "GEO": "33.8688,151.2093,300km",
        "GEO_NAME": "SYDNEY"

    },
    {
        "ACCOUNT_NAME": "AD1",
        "ACCESS_TOKEN": "1388170110330806273-Vfxp4sE6mJNduZaA6WcgNiEkM20mfP",
        "ACCESS_TOKEN_SECRET": "LL89KuRd89IbmWmkyL4AKc2gDEGuy9MwjnNHWCFajRc1F",
        "CONSUMER_KEY": "IpYRKJ5BY42oQL9hmHxtTEyq5",
        "CONSUMER_SECRET": "LS5qy6yK3AZROZfK1a6VIYHVTk3ud32DnqlxUFlJ9pfF13njKr",
        "GEO": "35.2809,149.1300,300km",
        "GEO_NAME": "CANBERRA"
    },
    {
        "ACCOUNT_NAME": "EG1",
        "ACCESS_TOKEN": "1382859648613507072-8LT5wgyUWM15f1hPb4YemPY6nrONN4",
        "ACCESS_TOKEN_SECRET": "ki18Lz1taArtHKVmrfmTzgNqkzhUlj6abJ1m5HNgSqc7T",
        "CONSUMER_KEY": "IvftZ2VAvxMN2KTIO9VkfmArA",
        "CONSUMER_SECRET": "q6VDoNdo4IdxuHyBy60SVkpwsu0ImQsmvbUi6reZbOcXfsuHGo",
        "GEO": "12.4637,130.8444,300km",
        "GEO_NAME": "DARWIN"
    },
    {
        "ACCOUNT_NAME": "EG2",
        "ACCESS_TOKEN": "1388356373797171206-xro1a2wXQLQ9XRppkUaJoRHeNNPUIf",
        "ACCESS_TOKEN_SECRET": "jplA7qTRP5Ou4bombZVylanK5nLefFEl4sKp5lb2BL1ij",
        "CONSUMER_KEY": "sRqz4V2OdLOfpifO813ekzcOd",
        "CONSUMER_SECRET": "Dv6xpUVwCWEYH5mko04AH7mgpejBLjfhHyEYXl8b2NFhXlMjVg",
        "GEO": "27.4705,153.0260,300km",
        "GEO_NAME": "BRISBANE"
    }





]
#COUCH_URL = "http://admin:password@127.0.0.1:5984/"
COUCH_URL = "http://admin:mrcpasswordcouch@172.26.129.229:5984/"
LOOP_COUNT=150


def parse_and_store(db, tweet_json, index, geo_name, account_name):
    """
    This function parse the twitter json, creates a separate json object to store in couchDB
    :param db: couchDB instance
    :param tweet_json: json from twitter api
    :param index: partition index
    :return: None
    """
    id = None
    tweet_string = None
    try:
        id = tweet_json['id_str']
        tweet_string = json.dumps(tweet_json)

        # some of the fields are defined here with null values because, although the keys can get added in dictionary
        # dynamically, but some of them are conditional so might not get added. Initializing the keys with default values
        # ensures consistent structure and will help in data analysis
        json_data = {
            '_id': "partition" + str(index) + ":" + str(id),
            'tweet_id': tweet_json['id_str'],
            'created_at': tweet_json['created_at'],
            'text': tweet_json['text'],
            'source': tweet_json['source'],
            'lang': tweet_json['lang'],
            'reply_status_id':None,
            'reply_user_id':None,
            'reply_screen_name':None,
            'quoted':False,
            'retweeted':False,
            'retweet_count':None,
            'possibly_sensitive':False,
            'metadata_result_type':None,
            'user_id':None,
            'user_name':None,
            'user_screen_name':None,
            'user_location':None,
            'user_desc':None,
            'user_verified':False,
            'user_follower_count':None,
            'user_friend_count':None,
            'user_statuses_count':None,
            'user_created_at':None,
            'coordinates_lat':None,
            'coordinates_lng':None,
            'place_country':None,
            'place_country_code':None,
            'place_type':None,
            'place_name':None,
            'place_full_name':None,
            'hash_tags':None,
            'user_mentions':None,
            'geo_name':geo_name,
            'account_name':account_name,
            'stored_at': str(datetime.now())
        }

        try:
            json_data['reply_status_id']= tweet_json['in_reply_to_status_id']
            json_data['reply_user_id']= tweet_json['in_reply_to_user_id']
            json_data['reply_screen_name']= tweet_json['in_reply_to_screen_name']
            json_data['quoted']= tweet_json['is_quote_status']
            json_data['retweeted']= tweet_json['retweeted']
            json_data['possibly_sensitive']= tweet_json['possibly_sensitive']
        except KeyError as e:
            print(str(e))
        except:
            print("Error in parsing some tweet recount and quote data")

        try:
            if json_data['quoted']:
                json_data['quoted_id']= tweet_json['quoted_status_id_str']
                json_data['quote_count']= tweet_json['quote_count']
                json_data['quoted_status']= tweet_json['quoted_status']
        except KeyError as e:
            print(str(e))
        except:
            print("Error in parsing quoted data")

        try:
            if json_data['retweeted']:
                json_data['retweet_count'] = tweet_json['retweet_count']
                json_data['retweeted_status']= tweet_json['retweeted_status']
        except KeyError as e:
            print(str(e))
        except:
            print("Error in parsing retweeted data" )


        try:
            if tweet_json['metadata'] is not None:
                json_data['metadata_result_type']= tweet_json['metadata']['result_type']
        except KeyError as e:
            print(str(e))
        except:
            print("Error in parsing meta data:" + str(json.dumps(tweet_json['metadata'])))

        try:
            if tweet_json['user'] is not None:
                json_data['user_id'] = tweet_json['user']['id_str']
                json_data['user_name'] = tweet_json['user']['name']
                json_data['user_screen_name'] = tweet_json['user']['screen_name']
                json_data['user_location'] = tweet_json['user']['location']
                json_data['user_desc'] = tweet_json['user']['description']
                json_data['user_verified'] = tweet_json['user']['verified']
                json_data['user_follower_count'] = tweet_json['user']['followers_count']
                json_data['user_friend_count'] = tweet_json['user']['friends_count']
                json_data['user_statuses_count'] = tweet_json['user']['statuses_count']
                json_data['user_created_at']=  tweet_json['user']['created_at']
        except KeyError as e:
            print(str(e))
        except:
            print("Error in parsing user data: " + str(json.dumps(tweet_json['user'])))


        try:
            if tweet_json['coordinates'] is not None:
                if tweet_json['coordinates']['coordinates'] is not None:
                    json_data['coordinates_lat']= tweet_json['coordinates']['coordinates'][0]
                    json_data['coordinates_lng']= tweet_json['coordinates']['coordinates'][1]
        except KeyError as e:
            print(str(e))
        except:
            print("Error in parsing coordinate data :" + str(json.dumps(tweet_json['coordinates'])))

        try:
            if tweet_json['place'] is not None:
                json_data['place_country']= tweet_json['place']['country']
                json_data['place_country_code']= tweet_json['place']['country_code']
                json_data['place_type']= tweet_json['place']['place_type']
                json_data['place_name']= tweet_json['place']['name']
                json_data['place_full_name']= tweet_json['place']['full_name']
        except KeyError as e:
            print(str(e))
        except:
            print("Error in parsing place data : " + str(json.dumps(tweet_json['place'])))

        if tweet_json['entities'] is not None:
            json_data['hash_tags']= get_hash_tags(tweet_json['entities']['hashtags'])
            json_data['user_mentions']= get_user_mentions(tweet_json['entities']['user_mentions'])

        db.save(json_data)
        return id
    except:
        print("Error in saving the tweet id :" + str(id) + tweet_string)


def get_hash_tags(tweet_json_tags):
    tags = []
    try:
        for h in tweet_json_tags:
            tags.append(h['text'])
    except KeyError as e:
        print(str(e))
    except:
        print("Error in parsing hash tags : " + str(json.dumps(tweet_json_tags)))
    return  tags


def get_user_mentions(tweet_json_usermentions):
    mentions=[]
    try:
        for h in tweet_json_usermentions:
            mentions.append(h['screen_name'])
    except KeyError as e:
        print(str(e))
    except:
        print("Error in parsing user mentions: " + str(json.dumps(tweet_json_usermentions)))
    return  mentions

def fetch_tweet_data(db, db2 ):
    """
    This function iterates on various accounts and fetches the data from twitter
    :param db: couch db single instance connection
    :return: None
    """
    index = 0
    for tokens in token_list:
        try:
            last_fetched_changed = False
            last_fetched_id = None
            rev = None
            try:
                last_fetched_result = db2.get("last_fetched_id:" +tokens["ACCOUNT_NAME"])
                if last_fetched_result is not None:
                    rev = last_fetched_result["_rev"]
                    last_fetched_id = last_fetched_result["result"]
            except:
                print("last fetched twitter id not found, keeping it null")
            index += 1
            index = index % 5
            auth = tweepy.OAuthHandler(tokens["CONSUMER_KEY"], tokens["CONSUMER_SECRET"])
            auth.set_access_token(tokens["ACCESS_TOKEN"], tokens["ACCESS_TOKEN_SECRET"])

            api = tweepy.API(auth, wait_on_rate_limit=True)
            stats = tweepy.Cursor(api.search, geocode=tokens["GEO"], lang="en", since_id=last_fetched_id,
                                          count=LOOP_COUNT ).items(LOOP_COUNT)

            for s in stats:
                print("accountname: " + tokens["ACCOUNT_NAME"] + " , no of tweets: " + str(stats.num_tweets))
                if s._json is not None:
                    last_fetched_id = parse_and_store(db, s._json, index , tokens["GEO_NAME"],tokens["ACCOUNT_NAME"])
                    print("stored: " + str(last_fetched_id) + " accountname: " + tokens["ACCOUNT_NAME"])
                    last_fetched_changed = True
                    try:
                        if last_fetched_id is not None and last_fetched_changed:
                            if rev is None:
                                t = db2.save({'_id': "last_fetched_id:"+tokens["ACCOUNT_NAME"], 'result': last_fetched_id})
                                rev = t[1]
                            else:
                                t = db2.save({'_id': "last_fetched_id:"+tokens["ACCOUNT_NAME"], '_rev': rev, 'result': last_fetched_id})
                                rev = t[1]
                    except:
                        print("Error in saving last fetched id")
        except TweepError as e:
            print(str(e))
        except:
            print("Error in loop for account name  : " + tokens["ACCOUNT_NAME"])


def main():
    """
    This is the main function which calls the function to fetch Twitter Data and put a sleep timer for 15 mins due to
    Rate Limiting Restrictions of Twitter API
    :return: Nothing
    """
    couch = couchdb.Server(COUCH_URL)
    db = couch["twitterfeed"]
    db2 = couch["parsed_data"]
    try:
        while True:
            fetch_tweet_data(db, db2)
            time.sleep(15 * 60)
    except:
        print("Error")


main()