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
        "CONSUMER_SECRET": "4RDA9ZUsl0soZwePswYrF1hKWmZQRKfeAnG2hbTlR5IpJC4v3y"
    },
    {
        "ACCOUNT_NAME": "SM1",
        "ACCESS_TOKEN": "1385176748229160963-lAKIZyu6S4IWbGJ3PlWaj42Vib6KHl",
        "ACCESS_TOKEN_SECRET": "Uf3dPXCJ2eJE2MyHKX4qInSJJacQkFhz1pssESk5L4xfb",
        "CONSUMER_KEY": "1TWIf5dxovtRAgsewLnAMswVf",
        "CONSUMER_SECRET": "4Fqys3SJKUaXIs929qKxS6nLJI6hLkgmid5ugn1CrlrHuAtNQ2"
    }
]
COUCH_URL = "http://admin:password@127.0.0.1:5984/"


def parse_and_store(db, tweet_json, index):
    """
    This function parse the twitter json, creates a separate json object to store in couchDB
    :param db: couchDB instance
    :param tweet_json: json from twitter api
    :param index: partition index
    :return: None
    """

    id = tweet_json['id']
    db.save({'_id': "partition" + str(index) + ":" + str(id), 'result': json.dumps(tweet_json)})
    print(tweet_json)


def fetch_tweet_data(db):
    """
    This function iterates on various accounts and fetches the data from twitter
    :param db: couch db single instance connection
    :return: None
    """

    index = 0
    for tokens in token_list:
        try:
            index += 1
            auth = tweepy.OAuthHandler(tokens["CONSUMER_KEY"], tokens["CONSUMER_SECRET"])
            auth.set_access_token(tokens["ACCESS_TOKEN"], tokens["ACCESS_TOKEN_SECRET"])

            api = tweepy.API(auth, wait_on_rate_limit=True)
            g = "37.8136,144.9631,300km"
            # search_words = ["#covid19", "2020", "lockdown"]
            stats = tweepy.Cursor(api.search, geocode=g, lang="en", until="2021-04-21", count=1).items(1)
            for s in stats:
                parse_and_store(db, s._json, index)
        except :
            print("Error in loop for account name  : " + tokens["ACCOUNT_NAME"])


def main():
    """
    This is the main function which calls the function to fetch Twitter Data and put a sleep timer for 15 mins due to
    Rate Limiting Restrictions of Twitter API
    :return: Nothing
    """
    couch = couchdb.Server(COUCH_URL)
    db = couch["twitterfeed"]
    try:
        count = 0
        while count < 3333:
            count += 1
            fetch_tweet_data(db)
            time.sleep(15 * 60)
    except:
        print("Error")


main()