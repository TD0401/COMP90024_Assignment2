import json
import couchdb
import tweepy
import time


token_list = [
    {
        "ACCOUNT_NAME": "TD1",
        "ACCESS_TOKEN": "1382216257299095553-UFdedtyG9RMYPpJ5hrDi0bHaeBFsre",
        "ACCESS_TOKEN_SECRET": "aCTcoaD02YvgRBVHqvpupl51c26cpgB7MLqGNvjTdgYHY",
        "CONSUMER_KEY": "HzSYdI0t164WwtK6VI9WkVgn0",
        "CONSUMER_SECRET": "4RDA9ZUsl0soZwePswYrF1hKWmZQRKfeAnG2hbTlR5IpJC4v3y",
        "GEO":"37.8136,144.9631,300km",
        "GEO_NAME":"MELBOURNE"
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
        "ACCOUNT_NAME": "HM1",
        "ACCESS_TOKEN": "1387920378123591681-snwmk8qdEiOHxv0NUgi2xIf8g8TfyO",
        "ACCESS_TOKEN_SECRET": "oREGZrMLSthOHZo3Ss4nBa4Vczcp2Z5QndTMsxOjwA39n",
        "CONSUMER_KEY": "7xuNIF1O0V7qZ2wD1Vtw6FgEf",
        "CONSUMER_SECRET": "978A7k7jjBdRsiVyfRiSBIFfKKsBwEMvEatOgSN0liljvlGULr",
        "GEO": "31.9523,115.8613,300km",
        "GEO_NAME": "PERTH"
    },
    {
        "ACCOUNT_NAME": "HM2",
        "ACCESS_TOKEN": "2383562348-sGkphwZZf9f6fd1mudq5rLkB6uw7jlDjKY3aFpR",
        "ACCESS_TOKEN_SECRET": "XTLo3R8nwrAwRp1CIhHsBQ6ZIdS10RfxGlN7pCcLD2ojp",
        "CONSUMER_KEY": "QIfwUNGd1QUmSFG1YzNjR46ST",
        "CONSUMER_SECRET": "qyGwFSmCN3B38a9zbGh2MTfj3LiwQqaNr2wfSY4gl4ANT9vKtc",
        "GEO": "27.4705,153.0260,300km",
        "GEO_NAME": "BRISBANE"
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
        "GEO": "37.8136,144.9631,300km",
        "GEO_NAME": "MELBOURNE"
    }
]
COUCH_URL = "http://admin:password@127.0.0.1:5984/"
LOOP_COUNT=1


def parse_and_store(db, tweet_json, index):
    """
    This function parse the twitter json, creates a separate json object to store in couchDB
    :param db: couchDB instance
    :param tweet_json: json from twitter api
    :param index: partition index
    :return: None
    """


    try:
        id = tweet_json['id']
        json_data = {'_id': "partition" + str(index) + ":" + str(id),
                    'created_at':tweet_json['created_at'],
                     'text':tweet_json['text']
                     'hashtags':tweet_json['hastag']
                     "[user:id]":tweet_json['usr_id']
                     ## TODO: need to complete the json part
        }
        db.save(json_data)
        print(tweet_json)
    except:
        print('Error in saving in DB')


def fetch_tweet_data(db, db2, last_fetched_id):
    """
    This function iterates on various accounts and fetches the data from twitter
    :param db: couch db single instance connection
    :return: None
    """
    dbFoundLastFetched = True
    if last_fetched_id is None:
        dbFoundLastFetched = False
    index = 0
    for tokens in token_list:
        try:
            index += 1
            index = index % 5
            auth = tweepy.OAuthHandler(tokens["CONSUMER_KEY"], tokens["CONSUMER_SECRET"])
            auth.set_access_token(tokens["ACCESS_TOKEN"], tokens["ACCESS_TOKEN_SECRET"])

            api = tweepy.API(auth, wait_on_rate_limit=True)
            stats = None
            #if dbFoundLastFetched:
            #    stats = tweepy.Cursor(api.search, geocode=tokens["GEO"], lang="en",  count=LOOP_COUNT).items(LOOP_COUNT)
            #else:
            stats = tweepy.Cursor(api.search, geocode=tokens["GEO"], lang="en", since_id=last_fetched_id,
                                          count=LOOP_COUNT).items(LOOP_COUNT)
            for s in stats:
                parse_and_store(db, s._json, index)
                last_fetched_id = s._json['id']

            if dbFoundLastFetched:
                db2.update({'_id': "last_fetched_id" , 'result': last_fetched_id})
            else:
                db2.save({'_id': "last_fetched_id", 'result': last_fetched_id})
                dbFoundLastFetched = True
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
    last_fetched_id = None
    try:
        last_fetched_id = couch["parsed_data"].get("last_fetched_id")["result"]
    except:
        print("last fetched twitter id not found, keeping it null")
    try:
        while True:
            fetch_tweet_data(db,db2, last_fetched_id)
            time.sleep(15 * 60)
    except:
        print("Error")


main()