// ------------------------------
// Plethysmogram graph
// ------------------------------
var pleth = {
x: [1, 2, 3, 4],
y: [10, 15, 13, 17],
type: 'scatter'
};

var data = [pleth];
Plotly.newPlot('pleth', data);

// ------------------------------
// Heart Rate Variability graph
// ------------------------------
var hrv = {
x: [1, 2, 3, 4, 5, 6, 7, 8],
y: [10, 15, 13, 17, -1, -3, -4],
type: 'scatter'
};

var data1 = [hrv];
Plotly.newPlot('hrv', data1);

// ------------------------------
// Oxygen Saturation Value
// ------------------------------
var ox = {
  x: 90
};

// ------------------------------
// Heart Rate Frequency value
// ------------------------------
var hr = {
  x: 80
};

// ------------------------------
// Cardiac Output value
// ------------------------------
var co = {
  x: 4
};
