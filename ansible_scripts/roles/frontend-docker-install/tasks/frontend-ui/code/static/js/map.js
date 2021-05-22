const API_KEY = "pk.eyJ1IjoiZXpnYWxsbzg3IiwiYSI6ImNraWlqOWNkZzBhMTEyeW9kZTFsYWV2eXMifQ.FIAMf-ix0ER-CwPLhc02xg"

var map_data = "http://"+ ip_addr +"/api/dashboard/locationCountsByState"


function map_load(stateCode, lat, lng, zoom_level){
    url = map_data + "?stateCode=" + stateCode ;

    d3.json(url).then((data) =>{
         myMap = createFeatures(data,stateCode, lat, lng, zoom_level);
    });
}

function createFeatures(twitData,stateCode, lat,lng , zoom_level) {
  // Define a function we want to run once for each feature in the features array
  // Give each feature a popup describing the place and time of the earthquake
  function onEachFeature(feature, layer) {

    layer.bindPopup("<p>" + feature.properties.place +
      "</p><hr><p>" + feature.properties.count + "</p>");
  }

  // Create a GeoJSON layer containing the features array on the earthquakeData object
  // Run the onEachFeature function once for each piece of data in the array
  var twitts = L.geoJSON(twitData, {
    pointToLayer: function (feature, latlng) {
      var geojsonMarkerOptions = {
          radius: feature.properties.count/10000,
          fillColor: getColour(feature.properties.count),
          // color: 'white',
          weight: 1,
          opacity: 1,
          fillOpacity: 1
      };
      return L.circleMarker(latlng, geojsonMarkerOptions)
    },

    onEachFeature: onEachFeature
  });

  // Sending our earthquakes layer to the createMap function
  return createMap(twitts,stateCode, lat ,lng , zoom_level);
}

function createMap(twitter,stateCode, lat ,lng , zoom_level) {

    // Define streetmap and darkmap layers
    var streetmap = L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
      attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
      tileSize: 512,
      maxZoom: 18,
      zoomOffset: -1,
      id: "mapbox/streets-v11",
      accessToken: API_KEY
    });

    var darkmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
      maxZoom: 18,
      id: "dark-v10",
      accessToken: API_KEY
    });

    // Define a baseMaps object to hold our base layers
    var baseMaps = {
      "Street Map": streetmap,
      "Dark Map": darkmap
    };

    // Create overlay object to hold our overlay layer
    var overlayMaps = {
      Tweets: twitter
    };

    // Create our map, giving it the streetmap and earthquakes layers to display on load
    var myMap = L.map("mapCluster_" + stateCode, {
      center: [
        lat, lng
      ],
      zoom: zoom_level,
      layers: [darkmap, twitter]
    });

    // Create a layer control
    // Pass in our baseMaps and overlayMaps
    // Add the layer control to the map
    L.control.layers(baseMaps, overlayMaps, {
      collapsed: false
    }).addTo(myMap);

    return myMap;
}

function getColour(count) {
  switch (count) {
    case count > 100:
      return "#ce1212";
      break;
    case count > 60:
      return "#ce1212";
       break;
    case count >33:
      return "#e1881b";
      break;
    case count > 25:
      return "#eb961e";
      break;
    case count >18:
      return "#f9af3a";
      break;
    case count > 10:
      return "#f9c54e";
      break;
    case count > 5:
      return "#c8ba4a";
      break;
    default:
      return "#72147e"
  }
}


function call_sequence(){
    map_load('VIC',-37.80315, 144.89793 ,8);
    map_load('NSW',-33.87838, 151.11873 ,8);
    map_load('QLD',-27.46231, 153.01102,9);
    map_load('WA',-31.93725, 115.87361,9);
    map_load('NT',-12.59398, 131.09535,6);
    map_load('SA',-34.914905, 138.61250,9);
    map_load('TAS',-42.91996, 146.85878, 8);
}

call_sequence();
