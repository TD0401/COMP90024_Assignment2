import sys
from itertools import islice
import couchdb
import json
from datetime import datetime

#COUCH_URL = "http://admin:password@127.0.0.1:5984/"
COUCH_URL = "http://admin:mrcpasswordcouch@172.26.134.25:5984/"
couch = couchdb.Server(COUCH_URL)
db = couch["twitterfeed"]


def get_hash_tags(tweet_json_tags):
    tags = []
    try:
        for h in tweet_json_tags:
            tags.append(h['text'])
    except KeyError as e:
        print(str(e))
    except:
        print("Error in parsing hash tags : " + str(json.dumps(tweet_json_tags)))
    return tags


def get_user_mentions(tweet_json_usermentions):
    mentions=[]
    try:
        for h in tweet_json_usermentions:
            mentions.append(h['screen_name'])
    except KeyError as e:
        print(str(e))
    except:
        print("Error in parsing user mentions: " + str(json.dumps(tweet_json_usermentions)))
    return mentions


def parse_json(tweet_json, rank):
    id = None
    tweet_string = None
    try:
        id = tweet_json['id']
        tweet_string = json.dumps(tweet_json)

        # some of the fields are defined here with null values because, although the keys can get added in dictionary
        # dynamically, but some of them are conditional so might not get added. Initializing the keys with default values
        # ensures consistent structure and will help in data analysis
        json_data = {
            '_id': "partition" + str(rank%5) + ":" + str(id),
            'tweet_id': tweet_json['id'],
            'created_at': tweet_json['doc']['created_at'],
            'text': tweet_json['doc']['text'],
            'source': tweet_json['doc']['source'],
            'lang': tweet_json['doc']['lang'],
            'reply_status_id': None,
            'reply_user_id': None,
            'reply_screen_name':None,
            'quoted': False,
            'retweeted': tweet_json['doc']['retweeted'],
            'retweet_count': None ,
            'possibly_sensitive': None,
            'metadata_result_type': None,
            'user_id': None,
            'user_name': None,
            'user_screen_name': None,
            'user_location': None,
            'user_desc': None,
            'user_verified': False,
            'user_follower_count': None,
            'user_friend_count': None,
            'user_statuses_count': None,
            'user_created_at': None,
            'coordinates_lat': None,
            'coordinates_lng': None,
            'place_country': None,
            'place_country_code': None,
            'place_type': None,
            'place_name': None,
            'place_full_name': None,
            'hash_tags': None,
            'user_mentions': None,
            'geo_name': tweet_json['doc']['location'],
            'account_name': 'BT',
            'stored_at': str(datetime.now())
        }


        try:
            if json_data['retweeted']:
                json_data['retweet_count'] = tweet_json['doc']['retweet_count']
            json_data['possibly_sensitive'] = tweet_json['doc']['possibly_sensitive']
            json_data['reply_status_id'] = tweet_json['doc']['in_reply_to_status_id']
            json_data['reply_user_id'] = tweet_json['doc']['in_reply_to_user_id']
            json_data['reply_screen_name'] = tweet_json['doc']['in_reply_to_screen_name']
        except KeyError as e:
            print(str(e))
        except:
            print("Error in parsing retweeted data")

        try:
            if tweet_json['doc']['metadata'] is not None:
                json_data['metadata_result_type'] = tweet_json['doc']['metadata']['result_type']
        except KeyError as e:
            print(str(e))
        except:
            print("Error in parsing meta data:" + str(json.dumps(tweet_json['metadata'])))

        try:
            if tweet_json['doc']['user'] is not None:
                json_data['user_id'] = tweet_json['doc']['user']['id_str']
                json_data['user_name'] = tweet_json['doc']['user']['name']
                json_data['user_screen_name'] = tweet_json['doc']['user']['screen_name']
                json_data['user_location'] = tweet_json['doc']['user']['location']
                json_data['user_desc'] = tweet_json['doc']['user']['description']
                json_data['user_verified'] = tweet_json['doc']['user']['verified']
                json_data['user_follower_count'] = tweet_json['doc']['user']['followers_count']
                json_data['user_friend_count'] = tweet_json['doc']['user']['friends_count']
                json_data['user_statuses_count'] = tweet_json['doc']['user']['statuses_count']
                json_data['user_created_at'] = tweet_json['doc']['user']['created_at']
        except KeyError as e:
            print(str(e))
        except:
            print("Error in parsing user data: " + str(json.dumps(tweet_json['user'])))

        try:
            if tweet_json['value'] is not None and tweet_json['value']['geometry'] is not None:
                if tweet_json['value']['geometry']['coordinates'] is not None:
                    json_data['coordinates_lat'] = tweet_json['value']['geometry']['coordinates'][1]
                    json_data['coordinates_lng'] = tweet_json['value']['geometry']['coordinates'][0]
        except KeyError as e:
            print(str(e))
        except:
            print("Error in parsing coordinate data :" + str(json.dumps(tweet_json['coordinates'])))

        try:
            if tweet_json['doc']['place'] is not None:
                json_data['place_country'] = tweet_json['doc']['place']['country']
                json_data['place_country_code'] = tweet_json['doc']['place']['country_code']
                json_data['place_type'] = tweet_json['doc']['place']['place_type']
                json_data['place_name'] = tweet_json['doc']['place']['name']
                json_data['place_full_name'] = tweet_json['doc']['place']['full_name']
        except KeyError as e:
            print(str(e))
        except:
            print("Error in parsing place data : " + str(json.dumps(tweet_json['place'])))

        if tweet_json['doc']['entities'] is not None:
            json_data['hash_tags'] = get_hash_tags(tweet_json['doc']['entities']['hashtags'])
            json_data['user_mentions'] = get_user_mentions(tweet_json['doc']['entities']['user_mentions'])

        mango_query = {
            "selector": { "id": {"$eq": id}},
            "fields": ["_rev"],

        }
        db = couch['twitterfeed']


        status, headers, data = db.resource.post_json('_find', mango_query)
        if data is not None and data['docs'] is not None and len(data['docs']) > 0:
            rev = data['docs'][0]['_rev']
            json_data['_rev'] = rev
        db.save(json_data)
        return id
    except:
        print("Error in saving the tweet id :" + str(id) + tweet_string)

def read_files(start_index , increment):
    file_name = sys.argv[1]
    with open(file_name, "r") as file:
        lines = list(islice(file, start_index, start_index + increment))
        count = 0
        for line in lines:
            count = count + 1
            try:
                line = line.replace("\n", "").replace("\r", "")
                # not reading first line
                # not reading last line, parse all json in between
                if not (start_index == 0 and count == 1) and not line == "]}":
                    if line.endswith(","):
                        line = line[:-1]
                    data = json.loads(line)
                    parse_json(data,count)
            except:
                print("error in parsing particular line: ", str(start_index + count))


def main():
    line_size = int(int(sys.argv[2]) / 8)
    if int(sys.argv[2]) % 8 != 0:
        line_size += 1
    for i in range(0, 8):
        read_files(i * line_size, line_size)


# calls main method
main()