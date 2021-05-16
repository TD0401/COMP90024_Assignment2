import couchdb
from flask import Flask, jsonify
from flask import Response,json
from flask import Flask, render_template 
from flask_cors import CORS
import requests
from pprint import pprint

couch = couchdb.Server()
app = Flask(__name__)
CORS(app)

COUCH_URL = "http://admin:mrcpasswordcouch@172.26.134.25:5984/"
couch = couchdb.Server(COUCH_URL)
db = couch["twittertest"]

headers = {
        'Authorization': "Basic YWRtaW46bXJjcGFzc3dvcmRjb3VjaA=="
    }

@app.route("/dashboard")
def dashboard():

    return  render_template("dashboard.html")


##################################   STATE COUNT  #################################################
@app.route("/stateCounts", methods = ['GET'])
def stateCount():
    url = "http://172.26.134.25:5984/twittertest/_design/TweetCountLatLng/_view/countByState?reduce=true&group=true&update=lazy&skip=0&limit=100"
    r =requests.get(url, headers= headers)
    data = json.loads(r.text)
    
    state_count = []
    for element in data['rows']:
        state = element['key'][1]
        value = element["value"]
        
        summary = {
            "state": state,
            "value": value
        }
        
        state_count.append(summary)

    return jsonify(state_count)


##################################   MAP ###################################################
@app.route("/locationCounts", methods = ['GET'])
def markerCluster():
    
    limit = 1000
    skip = 0
    geoJson = []
    while True:
        url = "http://172.26.134.25:5984/twittertest/_design/TweetCountLatLng/_view/countByLatLng?reduce=true&group=true&update=lazy&skip=%s&limit=%s" % ( skip , limit)
        ""
        r =requests.get(url, headers= headers)
        if r.status_code == 200:
            if len(r.text) > 0:
                data = json.loads(r.text)
                for dictionary in data['rows']:

                    #first dictionary key
                    elements = dictionary['key']
                    lat = elements[0]
                    lng = elements[1]
                    place = elements[2]

                    #second dictionary key
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

##################################   DAY COUNT  #################################################

@app.route("/dailyCount", methods = ['GET'])
def dayCount():
    limit = 49
    skip = 0
    url = "http://172.26.134.25:5984/twittertest/_design/TweetCountLatLng/_view/countByDay?reduce=true&group=true&update=lazy&skip=%s&limit=%s" % ( skip , limit)
    r =requests.get(url, headers= headers)
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

##################################   HOURLY COUNT  #################################################
@app.route("/hourlyCount", methods = ['GET'])
def hourCount():
    limit = 144
    skip = 0
    url = "http://172.26.134.25:5984/twittertest/_design/TweetCountLatLng/_view/countByHour?reduce=true&group=true&update=lazy&skip=%s&limit=%s" % ( skip , limit)
    r =requests.get(url, headers= headers)
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
    app.run(debug=True)
            