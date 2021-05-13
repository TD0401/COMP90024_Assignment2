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

COUCH_URL = "http://admin:mrcpasswordcouch@172.26.129.229:5984/"
couch = couchdb.Server(COUCH_URL)
db = couch["twitterfeed"]


@app.route("/dashboard")
def dashboard():

    return  render_template("dashboard.html")

@app.route("/locationCounts", methods = ['GET'])
def markerCluster():
    headers = {
        'Authorization': "Basic YWRtaW46bXJjcGFzc3dvcmRjb3VjaA=="
    }

    paritionids = ['partition0', 'partition1', 'partition2', 'partition3', 'partition4']

    geoJson = []
    for partid in paritionids:
        
        limit = 1000
        skip = 0
        
        while True:
            url = "http://172.26.129.229:5984/twitterfeed/_partition/%s/_design/TweetCountLatLng/_view/countByLatLng?reduce=true&group=true&update=lazy&skip=%s&limit=%s" % (partid, skip , limit)
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
                        
                    
                    #pagination control
                    skip += limit
                
                    # print("*********************************")
                    # print(partid)
                    # pprint(geoJson)
                    # print(len(geoJson))
                    break
    
    return jsonify(geoJson)

if __name__ == '__main__':
    app.run(debug=True)
            