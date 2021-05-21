from flask import Flask, jsonify
from flask import json
from flask_cors import CORS
from flask import request
import requests
import couchdb

# initializing flask, setting up CORS to run on different ips
app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})
couch_url = "http://admin:mrcpasswordcouch@172.26.130.129:5984/"
couch = couchdb.Server(couch_url)
db = couch['parsed_data']

# setting up couch properties like base url with ip, database doc url, authorization key
headers = {'Authorization': "Basic YWRtaW46bXJjcGFzc3dvcmRjb3VjaA=="}
base_url = "http://172.26.130.129:5984"
database_doc_url = "/twitterfeed/_design/TweetCountLatLng/_view"

state_code ={ "VIC":"VID",
              "NSW":"NSX",
              "QLD":"QLE",
              "WA":"WB",
              "TAS":"TAT",
              "NT":"NU",
              "SA":"SB"
              }


@app.route("/api/dashboard/stateCounts", methods=['GET'])
def state_counts():
    """
    This api returns number of tweets per state
    :return: json data for state wise count
    """

    url = base_url + database_doc_url + "/countByState?reduce=true&group=true&update=lazy&skip=0&limit=100"
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)

    state_count = []
    for element in data['rows']:
        state = element['key'][0]
        value = element["value"]

        summary = {
            "state": state,
            "value": value
        }

        state_count.append(summary)

    return jsonify(state_count)


@app.route("/api/dashboard/locationCounts", methods=['GET'])
def marker_cluster():
    """
    This api returns number of tweets aggregated over lat lng
    rounded to 3 digits in couch map reduce
    :return: json data for lat lng wise counts
    """

    limit = 1
    skip_qs = request.args.get('skip', 0)
    skip = int(skip_qs)
    geoJson = []
    count = 1
    while count < 6:
        mango_query = {
            "selector": {"id": {"$gt": None}},
            "limit": 1,
            "skip": skip
        }
        status, headers, data = db.resource.post_json('_find', mango_query)
        if data is not None and data['docs'] is not None and len(data['docs']) > 0:
            for data_row in data['docs'][0]["rows"]:

                # first dictionary key
                elements = data_row['key']
                lat = elements[0]
                lng = elements[1]
                place = elements[2]

                # second dictionary key
                value = data_row['value']

                geojson_1 = {
                    "geometry": {"type": "Point", "coordinates": [lat, lng]},
                    "properties": {"count": value, "place": place},
                    "type": "Feature"
                }

                geoJson.append(geojson_1)


            else:
                break
        count += 1

    return jsonify(geoJson)


@app.route("/api/dashboard/dailyCount", methods=['GET'])
def day_count():
    """
    This api returns number of tweets per state aggregated over each day
    :return: json data for state vs day wise count
    """

    limit = 100
    skip = 0
    url = base_url + database_doc_url + "/countByDay?reduce=true&group=true&update=lazy&skip=%s&limit=%s" % (
    skip, limit)
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)
    daily_count = []
    for element in data['rows']:
        state = element['key'][0]
        day = element['key'][1]
        value = element["value"]

        summary = {
            "state": state,
            "day": day,
            "value": value
        }

        daily_count.append(summary)

    return jsonify(daily_count)


@app.route("/api/dashboard/hourlyCount", methods=['GET'])
def hour_count():
    """
    This api returns number of tweets per state aggregated over hour of the day
    :return: json data for state vs hourly count
    """

    limit = 200
    skip = 0
    url = base_url + database_doc_url + "/countByHour?reduce=true&group=true&update=lazy&skip=%s&limit=%s" % (
    skip, limit)
    r = requests.get(url, headers=headers)
    data = json.loads(r.text)
    hourly_count = []
    for element in data['rows']:
        state = element['key'][0]
        hour = element['key'][1]
        value = element["value"]

        summary = {
            "state": state,
            "hour": hour,
            "value": value
        }

        hourly_count.append(summary)

    return jsonify(hourly_count)


@app.route("/api/dashboard/locationCountsByState", methods=['GET'])
def marker_cluster_statewise():
    """
    This api returns number of tweets aggregated over lat lng
    rounded to 3 digits in couch map reduce
    :return: json data for lat lng wise counts
    """
    limit = 1000
    stateCode = request.args.get('stateCode', 0)
    skip = 0
    geoJson = []
    count = 1
    endKey = state_code.get(stateCode)
    while count < 10:
        url = base_url + database_doc_url + "/countByLatLngReduced?reduce=true&group=true&update=lazy&skip=%s&limit=%s&startkey=[\"%s\"]&endkey=[\"%s\"]" % (
            skip, limit, stateCode, endKey)
        r = requests.get(url, headers=headers)
        data = json.loads(r.text)
        if data is not None and data['rows'] is not None and len(data['rows']) > 0:
            for element in data['rows']:

                # first dictionary key
                elements = element['key']
                lat = elements[1]
                lng = elements[2]
                place = elements[3]

                # second dictionary key
                value = element['value']

                geojson_1 = {
                    "geometry": {"type": "Point", "coordinates": [lat, lng]},
                    "properties": {"count": value, "place": place},
                    "type": "Feature"
                }

                geoJson.append(geojson_1)

            skip += limit
        else:
            break
        count += 1

    return jsonify(geoJson)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

