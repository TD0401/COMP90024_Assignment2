const API_KEY = "pk.eyJ1IjoiZXpnYWxsbzg3IiwiYSI6ImNraWlqOWNkZzBhMTEyeW9kZTFsYWV2eXMifQ.FIAMf-ix0ER-CwPLhc02xg"

var state_count = "http://127.0.0.1:5000/stateCounts"
console.log(state_count);

var map_data = "http://127.0.0.1:5000/locationCounts"
var daily_count = "http://127.0.0.1:5000/dailyCount"
var hourly_count = "http://127.0.0.1:5000/hourlyCount"


function init(){
    
  // Read samples.json
  d3.json("static/data/plotlysamples.json").then((jsonObject) =>{
    d3.json(state_count).then((statesObject)=>{
      
      console.log(statesObject);
      // console.log(statesObject.map(object => object.state));
      d3.select("#selState").selectAll("option")
          .data(statesObject)
          .enter()
          .append('option')
          .html(statesObject => statesObject.state);
      
      // //////   DUMMY \\\\\\\\\\\\\\\\\\\\\\\\\
      // console.log("DUMMY DATA")
          
      // add all of the IDs to the drop down menu
      // d3.select("#selDataset").selectAll("option")
      //     .data(jsonObject.samples)
      //     .enter()
      //     .append('option')
      //     .html(samples => samples.id);
      
      // plotlyPlot("940");  
      
      stateCountPlot();
      daysPlotly("WA");
      hoursPlotly("WA");

      // Call updatePlotly() when a change takes place to the DOM
      d3.selectAll("#selState").on("change", updatePlotly);
      
    });     
  })
}

init()

//                                   UPDATE  PLOT                          \\
// This function is called when a dropdown menu item is selected
function updatePlotly() {
  // Read samples.json     
  // Use D3 to select the dropdown menu for IDs
  var state = d3.select("#selState").property("value");
  // statePlotly(datasetID);
  
  daysPlotly(state);
  hoursPlotly(state);
      
}


/////////////////////////////////////      Horizontal Bar Chart         \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ 
/////////////////////////////////////      DUMMY FUNCTION        \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ 

function plotlyPlot(id){
    
    d3.json("static/data/plotlysamples.json").then((jsonObject) =>{
        
        ////////////////////       CHARTING VARIABLES     \\\\\\\\\\\\\\\\\\\\\\\\\
      
        var filteredData = jsonObject.samples.filter(data => data.id.toString() === id);
        // console.log(filteredData)
        // console.log(jsonObject) 
        
        var sample_values = filteredData[0].sample_values  
        // console.log(sample_values);
    
        var otu_ids = filteredData[0].otu_ids
        var otu_labels = filteredData[0].otu_labels
        
        // zipping sample values and OTU ids so that I can know which ID belongs to which value when sorting
        // index 0 = sample_values ; index 1 = OTU_id
        var zip = sample_values.map((sv, i) =>{
            return [sv, otu_ids[i], otu_labels[i]]
        });
        
        // console.log(zip);
    
        //sorting by sample values
        var clean_data = zip.sort((a, b) => b[0] - a[0]).slice(0,10).reverse();
        // console.log("THIS IS CLEAN_DATA")
        // console.log(clean_data);
        
        sampleValues = clean_data.map(object => object[0]);
        console.log(sampleValues);
    
        outIDs = clean_data.map(object => `OTU ${object[1]}`);
        // console.log("THIS Y AXIS")
        // console.log(outIDs);
    
        hover_text = clean_data.map(object => object[2]);
        
      //   bar and pie chart for Dummy Graphs \\
        
        // Trace1 for bar charts
        var trace1 = {
            x: sampleValues,
            y: outIDs,
            text: hover_text,
            type: "bar",
            orientation: "h",    
        };
        
        var trace2 = {
            values: sampleValues,
            labels: outIDs,
            hovertext: hover_text,
            type: "pie",        
        };
        
        // data
        var dataBar = [trace1];
        var dataPie = [trace2];
        
        // Apply the group bar mode to the layout
        var layout = {
            title: `Top 10 OTU IDs for ID ${id}`,
            plot_bgcolor:"#dbf6e9",
            paper_bgcolor:"#dbf6e9"
        };
        
        // Render the plot to the div tag with id "bar"
        Plotly.newPlot("horzBar", dataBar, layout);
        
        // Render the plot to the div tag with id "pie"
        Plotly.newPlot("topicsPie", dataPie, layout);
    });
};
/////////////////////////////////////      END DUMMY FUNCTION         \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\ 

function stateCountPlot() {
  d3.json(state_count).then((statesObject)=>{
    
    
    sorted = statesObject.sort((a, b) => b.value - a.value).reverse();
    // console.log(sorted);
    var x_axis = sorted.map(object => object.value);
    // console.log(test);
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
        color: '#c6ebc9'
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
          size: 25
        }
      },
      plot_bgcolor:"rgba(0,0,0,0)",
      paper_bgcolor:"rgba(0,0,0,0)",
      xaxis: {
        title: {
          text:  "Total Tweet Count ",
          font:{
            family: 'Verdana, sans-serif',
            size: 17
          }
        }
      },
      yaxis: {
        // gridwidth: 2,
        title: {
          text:  "State",
          font:{
            family: 'Verdana, sans-serif',
            size: 17
          }
        }
      },
    };

    // Render the plot to the div tag with id "bar"
    Plotly.newPlot("horzBar", dataBar, layout);

  }); 
}


// ///////////////////////////////      Count by Day        \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

function daysPlotly(state) {

  d3.json(daily_count).then((object) => {
    
    var filteredData = object.filter(data => data.state.toString() === state);
    // console.log(filteredData);

    var x_axis = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"];
    
    // var y_axis = filteredData.map(data => data.value);
    // console.log(y_axis);
    
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
          color: '#008891'
          // width: 1
        }
      }];
    
    var layout = {
      title: {
        text: `Daily Tweet Count for ${state}`,
        font:{
          family: 'Verdana, sans-serif',
          size: 25,
        }
      },
      
      showlegend: false,
      xaxis: {
        tickangle: -45,
        title: {
          text:  "Day of Week ",
          font:{
            family: 'Verdana, sans-serif',
            size: 17
          }
        }
      },
      yaxis: {
        zeroline: false,
        gridwidth: 2,
        title: {
          text:  "Count",
          font:{
            family: 'Verdana, sans-serif',
            size: 17
          }
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
    console.log(filteredData);

    var x_axis = filteredData.map(data => data.hour);
    console.log(x_axis);

    var y_axis = filteredData.map(data => data.value);
    console.log(y_axis);

    var data = [
      {
        x: x_axis,
        y: y_axis,
        type: 'bar',
        marker: {
          // color: '#70af85'
          // color: '#008891'
          color: 'rgb(26, 88, 114)'
        }
      }];
    
    var layout = {
      title: {
        text:  `Hourly Tweet Count for ${state}`,
        font:{
          family: 'Verdana, sans-serif',
          size: 25
        }
      },
      showlegend: false,
      xaxis: {
        tickangle: -45,
        title: {
          text:  "Hour of the Day (24hr)",
          font:{
            family: 'Verdana, sans-serif',
            size: 17
          }
        }  
      },
      yaxis: {
        zeroline: false,
        gridwidth: 2,
        title: {
          text:  "Count",
          font:{
            family: 'Verdana, sans-serif',
            size: 17
          }
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




//////////////////////            MAP Cluster         \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

// Store our API endpoint inside queryUrl
// var queryUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson"

// Perform a GET request to the query URL
d3.json(map_data).then((data) =>{
  
  // console.log("INITIAL LOG");
  // console.log(data);

  // Once we get a response, send the data.features object to the createFeatures function
  // array of json objects 
  // var dataArray = data.features
  // console.log(dataArray);

  createFeatures(data);

});

function getColour(count) {
  // console.log(count);
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



function createFeatures(twitData) {

  // console.log("CREATE FEATURES");
  // console.log(twitData);
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
          radius: feature.properties.count/200,
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
  createMap(twitts);
}

function createMap(twitter) {

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
  
    // console.log(earthquakes);
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
      layers: [streetmap, twitter]
    });
  
    // Create a layer control
    // Pass in our baseMaps and overlayMaps
    // Add the layer control to the map
    L.control.layers(baseMaps, overlayMaps, {
      collapsed: false
    }).addTo(myMap); 
}