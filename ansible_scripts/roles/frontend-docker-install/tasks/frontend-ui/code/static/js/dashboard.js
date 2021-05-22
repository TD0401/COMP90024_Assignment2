const API_KEY = "pk.eyJ1IjoiZXpnYWxsbzg3IiwiYSI6ImNraWlqOWNkZzBhMTEyeW9kZTFsYWV2eXMifQ.FIAMf-ix0ER-CwPLhc02xg"

var state_count = "http://" + ip_addr + "/api/dashboard/stateCounts"
var map_data = "http://"+ ip_addr +"/api/dashboard/locationCounts"
var daily_count = "http://"+ ip_addr +"/api/dashboard/dailyCount"
var hourly_count = "http://"+ ip_addr +"/api/dashboard/hourlyCount"


function init(){

  // Read samples.json

    d3.json(state_count).then((statesObject)=>{

      d3.select("#selState").selectAll("option")
          .data(statesObject)
          .enter()
          .append('option')
          .html(statesObject => statesObject.state);

      stateCountPlot(statesObject);
      daysPlotly($("#selState").prop("selectedIndex", 0).val());
      hoursPlotly($("#selState").prop("selectedIndex", 0).val());

      // Call updatePlotly() when a change takes place to the DOM
      d3.selectAll("#selState").on("change", updatePlotly);

    });

}



//                                   UPDATE  PLOT                          \\
// This function is called when a dropdown menu item is selected
function updatePlotly() {
  // Read samples.json
  // Use D3 to select the dropdown menu for IDs
  var state = d3.select("#selState").property("value");

  daysPlotly(state);
  hoursPlotly(state);

}


/////////////////////////////////////      Horizontal Bar Chart         \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\


function stateCountPlot(statesObject) {



    sorted = statesObject.sort((a, b) => b.value - a.value).reverse();
    var x_axis = sorted.map(object => object.value);
    var y_axis = sorted.map(object => object.state);


    // Trace1 for bar charts
    var trace1 = {
      x: x_axis,
      y: y_axis,
      type: "bar",
      orientation: "h",
      marker: {
        // color: '#6ddccf'
        // color: 'rgb(26, 88, 114)'
        // color: '#008891'
        color: '#26a334'
        // width: 1
      }
    };

    // data
    var dataBar = [trace1];

    // Apply the group bar mode to the layout
    var layout = {
      title: {
        text:  `Tweet Count per State`,
        font:{
          family: 'Verdana, sans-serif',
          size: 25,
          color:'#fff'
        }

      },
      width: 500,
      plot_bgcolor:"rgba(0,0,0,0)",
      paper_bgcolor:"rgba(0,0,0,0)",
      xaxis: {
        title: {
          text:  "Total Tweet Count ",
          font:{
            family: 'Verdana, sans-serif',
            size: 17,
            color: '#a1a1a6'
          }
        },
        tickfont : {
            color : '#fff'
        }
      },
      yaxis: {
        // gridwidth: 2,
        title: {
          text:  "State",
          font:{
            family: 'Verdana, sans-serif',
            size: 17,
            color: '#a1a1a6'
          }
        },
        tickfont : {
            color : '#fff'
        }
      }
    };

    // Render the plot to the div tag with id "bar"
    Plotly.newPlot("horzBar", dataBar, layout);


}


// ///////////////////////////////      Count by Day        \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

function daysPlotly(state) {

  d3.json(daily_count).then((object) => {

    var filteredData = object.filter(data => data.state.toString() === state);

    var x_axis = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"];


    var mon = filteredData.filter(data=> data.day.toString() === "Mon")
    var monData = mon[0].value;

    var tue = filteredData.filter(data=> data.day.toString() === "Tue")
    var tueData = tue[0].value;

    var wed = filteredData.filter(data=> data.day.toString() === "Wed")
    var wedData = wed[0].value;

    var th = filteredData.filter(data=> data.day.toString() === "Thu")
    var thuData = th[0].value;

    var fr = filteredData.filter(data=> data.day.toString() === "Fri")
    var frData = fr[0].value;

    var sat = filteredData.filter(data=> data.day.toString() === "Sat")
    var satData = sat[0].value;

    var sun = filteredData.filter(data=> data.day.toString() === "Sun")
    var sunData = sun[0].value;

    var y_axis = [monData, tueData, wedData, thuData, frData, satData, sunData];

    var data = [
      {
        x: x_axis,
        y: y_axis,
        type: 'bar',
        marker: {
          // color: '#d8f8b7'
          // color: '#e8e9a1'
          // color: '#c6ebc9'
          color: '#ff5ea7'
          // width: 1
        }
      }];

    var layout = {
      title: {
        text: `Daily Tweet Count for ${state}`,
        font:{
          family: 'Verdana, sans-serif',
          size: 25,
          color: '#fff'
        }
      },
      width: 500,
      showlegend: false,
      xaxis: {
        tickangle: -45,
        title: {
          text:  "Day of Week ",
          font:{
            family: 'Verdana, sans-serif',
            size: 17,
             color: '#a1a1a6'
          }
        },
        tickfont : {
            color : '#fff'
        }
      },
      yaxis: {
        zeroline: false,
        gridwidth: 2,
        title: {
          text:  "Count",
          font:{
            family: 'Verdana, sans-serif',
            size: 17,
             color: '#a1a1a6'
          }
        },
        tickfont : {
            color : '#fff'
        }
      },
      bargap :0.05,
      plot_bgcolor:"rgba(0,0,0,0)",
      paper_bgcolor:"rgba(0,0,0,0)"
    };

    Plotly.newPlot('dayBars1', data, layout);
  });
}

// /////////////////////////////        Count by Hour        \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
function hoursPlotly(state){
  d3.json(hourly_count).then((object) => {

    var filteredData = object.filter(data => data.state.toString() === state);
    var x_axis = filteredData.map(data => data.hour);
    var y_axis = filteredData.map(data => data.value);

    var data = [
      {
        x: x_axis,
        y: y_axis,
        type: 'bar',
        marker: {
          // color: '#70af85'
          // color: '#008891'
          color: '#fe9439'
        }
      }];

    var layout = {
      title: {
        text:  `Hourly Tweet Count for ${state}`,
        font:{
          family: 'Verdana, sans-serif',
          size: 25,
          color: '#fff'
        }
      },
      showlegend: false,
      xaxis: {
        tickangle: -45,
        title: {
          text:  "Hour of the Day (24hr)",
          font:{
            family: 'Verdana, sans-serif',
            size: 17,
             color: '#a1a1a6'
          }
        },
        tickfont : {
            color : '#fff'
        }
      },
      yaxis: {
        zeroline: false,
        gridwidth: 2,
        title: {
          text:  "Count",
          font:{
            family: 'Verdana, sans-serif',
            size: 17,
             color: '#a1a1a6'
          }
        },
        tickfont : {
            color : '#fff'
        }
      },
      bargap :0.05,
      plot_bgcolor:"rgba(0,0,0,0)",
      paper_bgcolor:"rgba(0,0,0,0)"
    };

    Plotly.newPlot('hourBars2', data, layout);

  });
}



// ///////////////////////////          Topic Analysis       \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
var topicData = "static/data/topic.json";
d3.json(topicData).then((data) =>{
  var data = [{
    values: Object.values(data),
    labels: Object.keys(data),
    name: 'Tweet Count',
    hoverinfo: 'value',
    hole: .7,
    type: 'pie',
    textinfo: "label+percent",
    textfont:{ color:'#fff'},
    automargin: true,
    textposition: "outside",
  }];

  var layout = {
    title: {
      text:  `Topic Analysis`,
      font:{
        family: 'Verdana, sans-serif',
        size: 25,
        color:'#fff'
      },
    },

    showlegend: false,
    height: 500,
    width: 500,
    plot_bgcolor:"rgba(0,0,0,0)",
    paper_bgcolor:"rgba(0,0,0,0)"
  }

  Plotly.newPlot('topicsPie', data, layout);
})



//////////////////////            MAP Cluster         \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

function map_load(){
    url = map_data + "?skip=0";

    d3.json(url).then((data) =>{
         myMap = createFeatures(data);
         addFeatures(myMap);
    });
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

function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
}

async function addFeatures(myMap,twitData) {

    for ( i = 1 ; i < 10 ; i++){
        url = map_data + "?skip=" + i
        d3.json(url).then((twitData) =>{
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
          }).addTo(myMap);
        });

        await sleep(10000);



    }

}


function createFeatures(twitData) {
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
  return createMap(twitts);
}

function createMap(twitter) {

    var darkmap = L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
      attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
      maxZoom: 18,
      id: "dark-v10",
      accessToken: API_KEY
    });

    // Define a baseMaps object to hold our base layers
    var baseMaps = {
      "Dark Map": darkmap
    };

    // Create overlay object to hold our overlay layer
    var overlayMaps = {
      Tweets: twitter
    };

    // Create our map, giving it the streetmap and earthquakes layers to display on load
    var myMap = L.map("mapCluster", {
      center: [
        -30.2744, 140.7751
      ],
      zoom: 4,
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


function callsequence(){
    init();
    map_load();
}

callsequence();