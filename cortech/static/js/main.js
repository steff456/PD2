var heart_rate = [0];
var pleth = [];
var ox_sat = [];
var car_out = [];
var heart_rate_var = [];

function change_hr(v){
  heart_rate.push(v)
  updateChartHR(hr_chart, heart_rate);
}

function change_ox(v){
  ox_sat.push(v)
}

function change_pleth(v){
  pleth.push(v)
}

function change_co(v){
  car_out.push(v)
}

function change_hrv(v){
  heart_rate_var.push(v)
}

function webSocket(){
  var ws = new WebSocket("ws://localhost:8000/socket");

  ws.onmessage = function (event) {
    event = JSON.parse(event.data)
    console.log(event);
    metric = event["metric"];
    // time = event["time"];
    value = event["value"];
    // console.log(metric + ";" + time + ";" + value)
    if (metric === "MDC_PULS_OXIM_PULS_RATE"){
      console.log("Change in heart rate")
      change_hr(value)
    }
    if (metric === "MDC_PULS_OXIM_SAT_O2"){
      console.log("Change in oxygen sat")
      change_ox(value)
    }
    if (metric === "MDC_PULS_OXIM_PLETH"){
      console.log("Change in pleth")
      change_pleth(value)
    }
    if (metric === "MDC_PULS_OXIM_CO"){
      console.log("Change in CO")
      change_co(value)
    }
    if (metric === "MDC_PULS_OXIM_HRV"){
      console.log("Change in CO")
      change_hrv(value)
    }
    console.log(heart_rate.length + ";" + ox_sat.length + ";" + pleth.length + ";" + car_out.length + ";" + heart_rate_var.length)
  }
}

$( document ).ready(function() {
    console.log( "document loaded" );
    webSocket()
});

$( window ).on( "load", function() {
    console.log( "window loaded" );
    var dps = []; // dataPoints
    chart = new CanvasJS.Chart("hr_chart", {
      title :{
		  text: "Heart Rate Frequency"
	    },
	    axisY: {
		      includeZero: false
	    },
	    data: [{
		      type: "line",
		      dataPoints: heart_rate
	    }]
    });

    var xVal = 0;
    var yVal = 100;
    var updateInterval = 1000;
    var dataLength = 20; // number of dataPoints visible at any point

    var updateChart = function (count) {
	     count = count || 1;
	     for (var j = 0; j < count; j++) {
		       yVal = yVal +  Math.round(5 + Math.random() *(-5-5));
		       dps.push({
			          x: xVal,
			          y: yVal
		            });
		       xVal++;
	     }
	     if (dps.length > dataLength) {
		       dps.shift();
	     }
	     chart.render();
    };
    updateChart(dataLength);
    setInterval(function(){updateChart()}, updateInterval);
  }
);
