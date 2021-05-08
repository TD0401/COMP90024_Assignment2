const API_KEY = "pk.eyJ1IjoiZXpnYWxsbzg3IiwiYSI6ImNraWlqOWNkZzBhMTEyeW9kZTFsYWV2eXMifQ.FIAMf-ix0ER-CwPLhc02xg"

// dayBars1
// Display the default plot
function init(){
  
    // Read samples.json
    d3.json("static/data/plotlysamples.json").then((jsonObject) =>{
        
        console.log(jsonObject);  
          
        // add all of the IDs to the drop down menu
        d3.select("#selDataset").selectAll("option")
            .data(jsonObject.samples)
            .enter()
            .append('option')
            .html(samples => samples.id);
        
        plotlyPlot("940");  
    
        // Call updatePlotly() when a change takes place to the DOM
        d3.selectAll("#selDataset").on("change", updatePlotly);
    });  
}
  
init()


// This function is called when a dropdown menu item is selected
function updatePlotly() {
    // Read samples.json
    d3.json("static/data/plotlysamples.json").then((jsonObject) =>{
        
        // Use D3 to select the dropdown menu for IDs
        var datasetID = d3.select("#selDataset").property("value");
        console.log(datasetID);
  
        plotlyPlot(datasetID);
          
    });
}

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
        console.log("THIS IS CLEAN_DATA")
        console.log(clean_data);
        
        sampleValues = clean_data.map(object => object[0]);
        // console.log(x_axis);
    
        outIDs = clean_data.map(object => `OTU ${object[1]}`);
        // console.log(y_axis)
    
        hover_text = clean_data.map(object => object[2]);
        
        /////////////////////       BAR & PIE CHART     \\\\\\\\\\\\\\\\\\\\\\\\\\\\\
        
      
        // Trace1 for bar charts
        var trace1 = {
            x: sampleValues,
            y: outIDs,
            text: hover_text,
            type: "bar",
            orientation: "h"
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
            title: `Top 10 OTU IDs for ID ${id}`
        };
    
        // Render the plot to the div tag with id "bar"
        Plotly.newPlot("horzBar", dataBar, layout);
        
        // Render the plot to the div tag with id "pie"
        Plotly.newPlot("topicsPie", dataPie, layout);

    });
};

//////////////////////    mapCluster \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

// Store our API endpoint inside queryUrl
var queryUrl = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/significant_month.geojson"

// Perform a GET request to the query URL
d3.json(queryUrl).then((data) =>{
  
  console.log(data);
  // Once we get a response, send the data.features object to the createFeatures function
  // array of json objects 
  var dataArray = data.features
  console.log(dataArray);

  createFeatures(dataArray);

});

function getColour(magnitude) {
    var color = "";
    // if (magnitude > 7) {
    //   color = "red";
    // }
    // if (magnitude > 6) {
    //   color = "red";
    // }
    if (magnitude > 5) {
      color = "#e1881b";
    }
    else if (magnitude > 4) {
      color = "#eb961e";
    }
    else if (magnitude > 3) {
      color = "#f9af3a";
    }
    else if (magnitude > 2) {
      color = "#f9c54e";
    }
    else if (magnitude > 1) {
      color = "#c8ba4a";
    }
    else {
      color = "#a0b657";
    }

    return color;
}

function createFeatures(earthquakeData) {

  // Define a function we want to run once for each feature in the features array
  // Give each feature a popup describing the place and time of the earthquake
  function onEachFeature(feature, layer) {

    layer.bindPopup("<h3>" + feature.properties.place +
      "</h3><hr><p>" + new Date(feature.properties.time) + "</p>");
  }

  // Create a GeoJSON layer containing the features array on the earthquakeData object
  // Run the onEachFeature function once for each piece of data in the array  
  var earthquakes = L.geoJSON(earthquakeData, {
    pointToLayer: function (feature, latlng) {
      var geojsonMarkerOptions = {
          radius: feature.properties.mag*2,
          fillColor: getColour(feature.properties.mag),
          color: "black",
          weight: 1,
          opacity: 1,
          fillOpacity: 1
      };
      return L.circleMarker(latlng, geojsonMarkerOptions)
    },
    
    onEachFeature: onEachFeature
  });
  
  // Sending our earthquakes layer to the createMap function
  createMap(earthquakes);
}

function createMap(earthquakes) {

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
      Earthquakes: earthquakes
    };
  
    // Create our map, giving it the streetmap and earthquakes layers to display on load
    var myMap = L.map("mapCluster", {
      center: [
        37.09, -95.71
      ],
      zoom: 5,
      layers: [streetmap, earthquakes]
    });
  
    // Create a layer control
    // Pass in our baseMaps and overlayMaps
    // Add the layer control to the map
    L.control.layers(baseMaps, overlayMaps, {
      collapsed: false
    }).addTo(myMap); 
}