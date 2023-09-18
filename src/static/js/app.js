$(document).ready(function () {

  const homeUsagectx = document.getElementById("homeUsage").getContext("2d");
  const homeUsage = new Chart(homeUsagectx, {
    type: "bar",
    data: {
      datasets: [{
        label: "Home Power Consumption (W)",
        fill: "origin",
        spanGaps: false
      }],
    },
    options: {
      borderWidth: 1,
      borderColor: ['rgba(130, 182, 223, 1)',],
      backgroundColor: ['rgba(192, 224, 248, 1)',],
      elements: {
        point:{
            radius: 0
        }
      },
      plugins: {
        legend: {
            display: false,
        }
      },
      scales: {
        x: {
          type: "time",
          time: {
            unit: "minute",
            displayFormats: {
              minute: "HH:mm"
            }
          }
        },
        y: {
          text: "W",
          beginAtZero: true,
        }
      }
    },
  });

  const outputHomectx = document.getElementById("outputHome").getContext("2d");
  const outputHome = new Chart(outputHomectx, {
    type: "line",
    data: {
      datasets: [{
        label: "Output to Home (W)",
        fill: "origin",
        spanGaps: false
      }],
    },
    options: {
      borderWidth: 1,
      borderColor: ['rgba(130, 182, 223, 1)',],
      backgroundColor: ['rgba(192, 224, 248, 1)',],
      elements: {
        point:{
            radius: 0
        }
      },
      plugins: {
        legend: {
            display: false,
        }
      },
      scales: {
        x: {
          type: "time",
          time: {
            unit: "minute",
            displayFormats: {
              minute: "HH:mm"
            }
          }
        },
        y: {
          text: "W",
          beginAtZero: true,
        }
      }
    },
  });

  const solarInputctx = document.getElementById("solarInput").getContext("2d");
  const solarInput = new Chart(solarInputctx, {
    type: "line",
    data: {
      datasets: [{
        label: "Solar Input (W)",
        fill: "origin",
        spanGaps: false
      }],
    },
    options: {
      borderWidth: 1,
      borderColor: ['rgba(248, 212, 105, 1)',],
      backgroundColor: ['rgba(249, 236, 184, 1)',],
      elements: {
        point:{
            radius: 0
        }
      },
      plugins: {
        legend: {
            display: false,
        }
      },
      scales: {
        x: {
          type: "time",
          time: {
            unit: "minute",
            displayFormats: {
              minute: "HH:mm"
            }
          }
        },
        y: {
          beginAtZero: true,
        }
      }
    },
  });

  const outputPackctx = document.getElementById("outputPack").getContext("2d");
  const outputPack = new Chart(outputPackctx, {
    type: "line",
    data: {
      datasets: [{
        label: "Charging/Discharging (W)",
        fill: "origin",
        spanGaps: false
      }],
    },
    options: {
      borderWidth: 1,
      borderColor: ['rgba(95, 170, 145, 1)',],
      backgroundColor: ['rgba(175, 218, 208, 1)',],
      elements: {
        point:{
            radius: 0
        }
      },
      plugins: {
        legend: {
            display: false,
        }
      },
      scales: {
        x: {
          type: "time",
          time: {
            unit: "minute",
            displayFormats: {
              minute: "HH:mm"
            }
          }
        },
        y: {
          beginAtZero: true
        }
      }
    },
  });

  const maxTempctx = document.getElementById("maxTemp").getContext("2d");
  const maxTemp = new Chart(maxTempctx, {
    type: "bar",
    data: {
      datasets: [{ label: "Battery Temperature",  }],
    },
    plugins: [ChartDataLabels],
    options: {
      borderWidth: 1,
      borderColor: ['rgba(98, 214, 158, 1)',],
      backgroundColor: ['rgba(98, 214, 158, 1)',],
      plugins: {
        legend: {
            display: false,
        },
        datalabels: {
          anchor: "end",
          align: "top",
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 75,
          grid: {
            drawBorder: false,
            display: false,
          },
          ticks: {
            display: false
          }
        },
        x: {
          grid: {
            drawBorder: false,
            display: false,
          },
        }
      }
    }
  });

  const socLevelctx = document.getElementById("socLevel").getContext("2d");
  const socLevel = new Chart(socLevelctx, {
    type: "bar",
    data: {
      datasets: [
        { 
          label: "State of Charge",
          borderRadius: 7,
          borderSkipped: "bottom"
        }
      ],
    },
    plugins: [ChartDataLabels],
    options: {
      borderWidth: 1,
      borderColor: ['rgba(98, 214, 158, 1)',],
      backgroundColor: ['rgba(98, 214, 158, 1)',],
      plugins: {
        legend: {
            display: false,
        },
        datalabels: {
          anchor: "end",
          align: "top",
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 120,
          grid: {
            drawBorder: false,
            display: false,
          },
          ticks: {
            display: false
          }
        },
        x: {
          grid: {
            drawBorder: false,
            display: false,
          },
        }
      }
    },
  });

  function getTimeSeriesLabels() {
    ts = []
    now = Date.now()
    ts.push(now)
    for (i=0; i++; i<30) {
      ts.unshift(now-60)
    }

  }

  const batteryPowerctx = document.getElementById("batteryPower").getContext("2d");
  const timeseries_labels = getTimeSeriesLabels();
  const batteryPower = new Chart(batteryPowerctx, {
    type: "bar",
    data: {
      datasets: [
        {
          label: '',
          borderColor: 'rgb(255, 0, 0)',
        },
        {
          label: '',
          borderColor: 'rgb(0, 255, 0)',
        }, 
        {
          label: '',
          borderColor: 'rgb(0, 0, 255)',
        },
        {
          label: '',
          orderColor: 'rgb(0, 0, 0)',
        }
      ],
    },
    options: {
      borderWidth: 1,
      borderColor: ['rgba(95, 170, 145, 1)',],
      backgroundColor: ['rgba(175, 218, 208, 1)',],
      elements: {
        point:{
            radius: 0
        }
      },
      plugins: {
        legend: {
            display: false,
        }
      },
      scales: {
        x: {
          type: "time",
          time: {
            unit: "minute",
            displayFormats: {
              minute: "HH:mm"
            }
          },
          ticks: {
            source: "auto"
          }
        },
        y: {
          stacked: false,
          beginAtZero: true
        }
      }
    },
  });


  const minVolctx = document.getElementById("minVol").getContext("2d");
  const minVol = new Chart(minVolctx, {
    type: "bar",
    data: {
      datasets: [
        { 
          label: "Min Cell Voltage",
          borderRadius: 7,
          borderSkipped: "bottom"
        }
      ],
    },
    plugins: [ChartDataLabels],
    options: {
      borderWidth: 1,
      borderColor: ['rgba(98, 214, 158, 1)',],
      backgroundColor: ['rgba(98, 214, 158, 1)',],
      plugins: {
        legend: {
            display: false,
        },
        datalabels: {
          anchor: "end",
          align: "top",
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          grid: {
            drawBorder: false,
            display: false,
          },
          ticks: {
            display: false
          }
        },
        x: {
          grid: {
            drawBorder: false,
            display: false,
          },
        }
      }
    },
  });


  const maxVolctx = document.getElementById("maxVol").getContext("2d");
  const maxVol = new Chart(maxVolctx, {
    type: "bar",
    data: {
      datasets: [
        { 
          label: "Max Cell Voltage",
          borderRadius: 7,
          borderSkipped: "bottom"
        }
      ],
    },
    plugins: [ChartDataLabels],
    options: {
      borderWidth: 1,
      borderColor: ['rgba(98, 214, 158, 1)',],
      backgroundColor: ['rgba(98, 214, 158, 1)',],
      plugins: {
        legend: {
            display: false,
        },
        datalabels: {
          anchor: "end",
          align: "top",
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          grid: {
            drawBorder: false,
            display: false,
          },
          ticks: {
            display: false
          }
        },
        x: {
          grid: {
            drawBorder: false,
            display: false,
          },
        }
      }
    },
  });


  const totalVolctx = document.getElementById("totalVol").getContext("2d");
  const totalVol = new Chart(totalVolctx, {
    type: "bar",
    data: {
      datasets: [
        { 
          label: "Battery Voltage",
          borderRadius: 7,
          borderSkipped: "bottom"
        }
      ],
    },
    plugins: [ChartDataLabels],
    options: {
      borderWidth: 1,
      borderColor: ['rgba(98, 214, 158, 1)',],
      backgroundColor: ['rgba(98, 214, 158, 1)',],
      plugins: {
        legend: {
            display: false,
        },
        datalabels: {
          anchor: "end",
          align: "top",
        }
      },
      scales: {
        y: {
          beginAtZero: true,
          max: 100,
          grid: {
            drawBorder: false,
            display: false,
          },
          ticks: {
            display: false
          }
        },
        x: {
          grid: {
            drawBorder: false,
            display: false,
          },
        }
      }
    },
  });

  $('#form-outputHomeLimit').on('submit', function () {
    socket.emit('setLimit', '{"property": "outputLimit", "value":' + $('#outputHomeLimit').val() +'}' );
    return false;
  });

  $('#form-solarInputLimit').on('submit', function () {
    socket.emit('setLimit', '{"property": "inputLimit", "value":' + $('#solarInputLimit').val() +'}' );
    return false;
  });

  $('#form-socSet').on('submit', function () {
    socket.emit('setLimit', '{"property": "socSet", "value":' + $('#socSet').val()*10 +'}' );
    return false;
  });

  $('#form-minSoc').on('submit', function () {
    socket.emit('setLimit', '{"property": "minSoc", "value":' + $('#minSoc').val()*10 +'}' );
    return false;
  });

  function updateCurValues(metric, data){
    document.getElementById("cur-" + metric).textContent = data
  }

  function seriesExists(datasets, label) {
    for (dataset of datasets) {
      if (label == dataset.label) {
        return true
      }
    }
  }

  function addData(label, metric, data, series) {
    singletons = ["socLevel","maxTemp","totalVol","minVol","maxVol"]
    remove = false
    chart = Chart.getChart(metric);

    if (singletons.includes(metric)) {
      idx = chart.data.labels.indexOf(label)
      remove = (idx >= 0)
      if (remove) {
        chart.data.labels.splice(idx,1)
      }
    }

    // if its a timeseries chart make sure we only display 30minutes
    timeseries = ["outputHome","solarInput","outputPack","electricLevel","batteryPower"]
    if (timeseries.includes(metric)) {
      chart.options.scales.x.min = Date.now()-900000
    }

    chart = Chart.getChart(metric);

    exists = false
    if (series != '') {
      exists = seriesExists(chart.data.datasets, series)
    }

    for (const [i, dataset] of chart.data.datasets.entries()) {
      if (i == 0) {
        chart.data.labels.push(label);
        //console.log("Idx: "+i+" label: "+label+ " dataset: "+dataset)
      }
      if (remove) {
        dataset.data.splice(idx,1)
      }
      if (series !=  '') {
        date = new Date(label);
        dateFormat = date.getHours() + ":" + date.getMinutes() + ":" + date.getSeconds()
        if (dataset.label == series) {
          //console.log("Dataset update: " + dateFormat +" " + series)
          //console.log(chart.data.labels)
          dataset.data.push(data);
        }
        if ((dataset.label == '') && (!exists)) {
          //console.log("Dataset add label: " + dateFormat +" " + series)
          dataset.label = series
          dataset.data.push(data);
          break
        }
      } else {
        dataset.data.push(data);
      }

      // for those where we only display one value sort it by label
      if (singletons.includes(metric)) {
        chart.data.labels.sort(sortDps())
        //console.log(eval(metric).data.labels)
      }
    }
    chart.update();
  }

  function sortDps(){
    return function(a, b){
      //console.log("Comparing: " + a + " : " + b)
      if(a.label < b.label){
        return 1;
      }else if(a.label > b.label){
        return -1;
      }else{
        return 0;   
      }
    }
  }

  function removeFirstData(metric) {
    chart = Chart.getChart(metric);
    chart.data.labels.splice(0, 1);
    chart.data.datasets.forEach((dataset) => {
      dataset.data.shift();
    });
  }

  const MAX_DATA_COUNT = 2000;
  var socket = io.connect();

  //receive details from server
  socket.on("updateSensorData", function (msg) {
    //console.log("Received sensorData: "+ msg.date + "::" + msg.metric + " :: " + msg.value);

    // Show only MAX_DATA_COUNT data
    charts = ["outputHome","solarInput","outputPack","batteryPower","totalVol","maxVol","minVol","maxTemp","socLevel","homeUsage"]
    if (charts.includes(msg.metric)) {
      chart = Chart.getChart(msg.metric);
      if (chart.data.labels.length > MAX_DATA_COUNT) {
        removeFirstData(msg.metric);
      }
      addData(msg.date, msg.metric, msg.value, msg.sn || "");
    }

    timeseries = ["outputHome","solarInput","outputPack","electricLevel","homeUsage"]
    if (timeseries.includes(msg.metric)) {
      updateCurValues(msg.metric, msg.value)
    }
  });

  socket.on("updateLimit", function(msg) {
    document.getElementById("state-" + msg.property).innerHTML = msg.value
  });
});