var heart_rate = [0];
var pleth = [0];
var ox_sat = [0];
var car_out = [0];
var heart_rate_var = [0];
var ws = new WebSocket("ws://localhost:8000/socket");

console.log(config);

ws.onmessage = function (event) {
  event = JSON.parse(event.data)
  console.log(event);
  metric = event["metric"];
  // time = event["time"];
  value = event["value"];
  // console.log(metric + ";" + time + ";" + value)
  if (metric === "MDC_PULS_OXIM_PULS_RATE"){
    console.log("Change in heart rate")
    heart_rate.push(value);
    config.data.labels.push(heart_rate.length);
    config.data.datasets[1].data.push(value);
    window.myLine.update();
    // change_hr(value)
  }
  if (metric === "MDC_PULS_OXIM_SAT_O2"){
    console.log("Change in oxygen sat")
    // change_ox(value)
    ox_sat.push(value);
    // config.data.labels.push(ox_sat.length);
    config.data.datasets[0].data.push(value);
    window.myLine.update();
  }
  if (metric === "MDC_PULS_OXIM_PLETH"){
    console.log("Change in pleth")
    // change_pleth(value)
  }
  if (metric === "MDC_PULS_OXIM_CO"){
    console.log("Change in CO")
    // change_co(value)
  }
  if (metric === "MDC_PULS_OXIM_HRV"){
    console.log("Change in CO")
    // change_hrv(value)
  }
}
