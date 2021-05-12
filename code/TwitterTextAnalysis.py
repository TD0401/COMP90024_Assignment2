import couchdb
import json


def process_json(doc):
    parsed_lines = 0
    with open("victoriaTweet.json", "a+") as file:
        for row in doc:
            if -39.3 <= row['coordinates_lat'] <= -33.8:
                if 140.6 < row['coordinates_lng'] < 150.3:
                    file.writelines(json.dumps(row))
                    file.writelines(",\n")
                    parsed_lines += 1

    return parsed_lines


def main():
    couch_url = "http://admin:mrcpasswordcouch@172.26.129.229:5984/"
    couch = couchdb.Server(couch_url)
    row_limit = 5
    bookmark = None
    rows_parse = 0
    rows_fetch = 0
    error_count = 0
    with open("victoriaTweet.json", "a+") as file:
        file.writelines("[\n")
    while error_count < 3:
        try:

            mango_query = {
                "selector": {"coordinates_lat": {"$gt": -39.3}, "coordinates_lng": {"$ne": None}, "lang": {"$eq": "en"}},
                "fields": ["text", "coordinates_lat", "coordinates_lng"],
                "limit": row_limit,
                "bookmark": bookmark
            }
            print(mango_query)
            db = couch['twitterfeed']
            status, headers, data = db.resource.post_json('_find', mango_query)
            bookmark = data['bookmark']
            if data is not None and data['docs'] is not None and len(data['docs']) > 0:
                rows_fetch += len(data['docs'])
                rows_parse += process_json(data['docs'])
                print("total rows fetched :" + str(rows_fetch) + ", total rows parsed:" + str(rows_parse) + ", last bookmark:" + bookmark)
            else:
                print('last bookmark: ' + bookmark)
                break
        except:
            print("error in parsing rows : " + str(rows_fetch) + " - " + str(rows_fetch + row_limit) + ", last bookmark:" + bookmark)
            error_count += 1

    with open("victoriaTweet.json", "a+") as file:
        file.writelines("]\n")

main()