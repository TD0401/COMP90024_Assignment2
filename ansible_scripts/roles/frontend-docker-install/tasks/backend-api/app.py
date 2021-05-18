from flask import Flask, jsonify
from flask import json
from flask_cors import CORS
from flask import request
import requests


# initializing flask, setting up CORS to run on different ips
app = Flask(__name__)
CORS(app, resources={r"*": {"origins": "*"}})

# setting up couch properties like base url with ip, database doc url, authorization key
headers = {'Authorization': "Basic YWRtaW46bXJjcGFzc3dvcmRjb3VjaA=="}
base_url = "http://172.26.130.129:5984"
database_doc_url = "/twitterfeed/_design/TweetCountLatLng/_view"


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

    limit = 5000
    skip_qs = request.args.get('skip', 0)
    skip = int(skip_qs)
    geoJson = []
    while True:
        url = base_url + database_doc_url + "/countByLatLng?reduce=true&group=true&update=lazy&skip=%s&limit=%s" % (
        skip, limit)
        ""
        r = requests.get(url, headers=headers)
        if r.status_code == 200:
            if len(r.text) > 0:
                data = json.loads(r.text)
                for dictionary in data['rows']:
                    # first dictionary key
                    elements = dictionary['key']
                    lat = elements[0]
                    lng = elements[1]
                    place = elements[2]

                    # second dictionary key
                    value = dictionary['value']

                    geojson_1 = {
                        "geometry": {"type": "Point", "coordinates": [lat, lng]},
                        "properties": {"count": value, "place": place},
                        "type": "Feature"
                    }

                    geoJson.append(geojson_1)

                skip += limit
            break

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


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

