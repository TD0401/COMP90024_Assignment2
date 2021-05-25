// API key
const API_KEY = "pk.eyJ1IjoiZXpnYWxsbzg3IiwiYSI6ImNraWlqOWNkZzBhMTEyeW9kZTFsYWV2eXMifQ.FIAMf-ix0ER-CwPLhc02xg"

// // Creating map object
// var myMap = L.map("map", {
//     center: [-30.2744, 140.7751],
//     zoom: 3
// });
  
// // Adding tile layer
// L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
//   attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
//   tileSize: 512,
//   maxZoom: 18,
//   zoomOffset: -1,
//   id: "mapbox/streets-v11",
//   accessToken: API_KEY
// }).addTo(myMap);

// // Load in geojson data
// var geoDataTest = "static/data/Median_Household_Income_2016.geojson";
// // console.log(geoDataTest);

// // var geoData ="static/data/spatial_data.json"
// // console.log(geoData);

// var geoData = "static/data/newchoropleth.geojson"
// // var geoData2 = "static/data/choropleth2.geojson"

// // Grab data with d3
// d3.json(geoDataTest, function(data) {

//   // console.log("this is geoData");
//   console.log(data);

//   // Create a new choropleth layer
//   geojson = L.choropleth(data, {

//     // Define what  property in the features to use
//     valueProperty: "MHI2016",

//     // Set color scale
//     scale: ["#ffffb2", "#b10026"],

//     // Number of breaks in step range
//     steps: 10,

//     // q for quartile, e for equidistant, k for k-means
//     mode: "q",
//     style: {
//       // Border color
//       color: "#fff",
//       weight: 1,
//       fillOpacity: 0.8
//     },

//     // Binding a pop-up to each layer
//     onEachFeature: function(feature, layer) {
//       layer.bindPopup("Zip Code: " + feature.properties.ZIP + "<br>Median Household Income:<br>" +
//         "$" + feature.properties.MHI2016);
//     }
//   }).addTo(myMap);

//   // Set up the legend
//   var legend = L.control({ position: "bottomright" });
//   legend.onAdd = function() {
//     var div = L.DomUtil.create("div", "info legend");
//     var limits = geojson.options.limits;
//     var colors = geojson.options.colors;
//     var labels = [];

//     // Add min & max
//     var legendInfo = "<h3>Median Income</h3>" +
//       "<div class=\"labels\">" +
//         "<div class=\"min\">" + limits[0] + "</div>" +
//         "<div class=\"max\">" + limits[limits.length - 1] + "</div>" +
//       "</div>";

//     div.innerHTML = legendInfo;

//     limits.forEach(function(limit, index) {
//       labels.push("<li style=\"background-color: " + colors[index] + "\"></li>");
//     });

//     div.innerHTML += "<ul>" + labels.join("") + "</ul>";
//     return div;
//   };

//   // Adding legend to the map
//   legend.addTo(myMap);

//   d3.json(geoData, function(data2){
//     console.log("This is new GeoJson");
//     console.log(data2);
//   });

// });

// ///////////////////////////////////////////////           FUNCTIONING CHOROPLETH \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
// / Creating map object
var myMap = L.map("map", {
  center: [-37.2744, 145.7751],
  zoom: 7
});

// Adding tile layer
L.tileLayer("https://api.mapbox.com/styles/v1/mapbox/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  // id: "mapbox/streets-v11",
  id: "dark-v10",
  accessToken: API_KEY
}).addTo(myMap);

// Load in geojson data
//var geoData = "static/data/Median_Household_Income_2016.geojson";
// console.log(geoData);
//var geoData2 = "static/data/newchoropleth.geojson"
var geoData3 = "static/data/choropleth3.geojson"


var geojson;

// Grab data with d3
d3.json(geoData3, function(data) {

  console.log(data);

  // Create a new choropleth layer
  geojson = L.choropleth(data, {
    
    // Define what  property in the features to use
    valueProperty: "sentiment",

    // Set color scale
    scale: ["#d1d9d9","#9fe6a0", "#aa2ee6"],

    // Number of breaks in step range
    steps: 10,

    // q for quartile, e for equidistant, k for k-means
    mode: "q",
    style: {
      // Border color
      color: "#fff",
      weight: 1,
      fillOpacity: 0.8
    },

    // Binding a pop-up to each layer
    onEachFeature: function(feature, layer) {
      layer.bindPopup("Sentiment value: " + feature.properties.sentiment + "<br/>Median Income: " +
        "$" + feature.properties.median_income + "<br/>Sleep: " + feature.properties.sleep + "<br/>Unemployment Rate: " + feature.properties.unemploy_rate + 
        "<br/>Work Life: " + feature.properties.worklife);
    }
  }).addTo(myMap);


  // Set up the legend
  var legend = L.control({ position: "bottomright" });
  legend.onAdd = function() {
    var div = L.DomUtil.create("div", "info legend");
    var limits = geojson.options.limits;
    console.log(limits);
    var colors = geojson.options.colors;
    var labels = [];

    // Add min & max
    var legendInfo = "<h1>Sentiment Analysis</h1>" +
      "<div class=\"labels\">" +
        "<div class=\"min\">" + limits[0] + "</div>" +
        "<div class=\"max\">" + limits[limits.length - 1] + "</div>" +
      "</div>";

    div.innerHTML = legendInfo;

    limits.forEach(function(limit, index) {
      labels.push("<li style=\"background-color: " + colors[index] + "\"></li>");
    });

    div.innerHTML += "<ul>" + labels.join("") + "</ul>";
    return div;
  };

  // Adding legend to the map
  legend.addTo(myMap);

  console.log(legend);


});