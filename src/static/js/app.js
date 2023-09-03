$(document).ready(function () {

  const outputHomectx = document.getElementById("outputHome").getContext("2d");
  const outputHome = new Chart(outputHomectx, {
    type: "line",
    data: {
      datasets: [{ label: "Output to Home (W)"}, {fill: "origin"}],
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
      datasets: [{ label: "Solar Input (W)"}, {fill: "origin"}],
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
      datasets: [{ label: "Charging/Discharging (W)"}, {fill: "origin"}],
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

  const electricLevelctx = document.getElementById("electricLevel").getContext("2d");
  const electricLevel = new Chart(electricLevelctx, {
    type: "line",
    tension: 0.4,
    data: {
      datasets: [{ label: "Average Battery Level" }, {fill: "origin"}],
    },
    options: {
      borderWidth: 1,
      borderColor: ['rgba(98, 214, 158, 1)',],
      backgroundColor: ['rgba(98, 214, 158, 1)',],
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
          max: 100,
          title: "˚C"
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
          label: "Battery State of Charge",
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

  function addData(label, metric, data) {
    singletons = ["socLevel","maxTemp","totalVol","minVol","maxVol"]
    remove = false
    if (singletons.includes(metric)) {
      idx = eval(metric).data.labels.indexOf(label)
      remove = (idx >= 0)
      if (remove) {
        eval(metric).data.labels.splice(idx,1)
      }
    }
    eval(metric).data.labels.push(label);

    // if its a timeseries chart make sure we only display 30minutes
    timeseries = ["outputHome","solarInput","outputPack","electricLevel"]
    if (timeseries.includes(metric)) {
      eval(metric).options.scales.x.min = Date.now()-900000
    }

    eval(metric).data.datasets.forEach((dataset) => {
      if (remove) {
        dataset.data.splice(idx,1)
      }
      dataset.data.push(data);
      // for those where we only display one value sort it by label
      if (singletons.includes(metric)) {
        eval(metric).data.labels.sort(sortDps())
        //console.log(eval(metric).data.labels)
      }
    });
    eval(metric).update();
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
    eval(metric).data.labels.splice(0, 1);
    eval(metric).data.datasets.forEach((dataset) => {
      dataset.data.shift();
    });
  }

  const MAX_DATA_COUNT = 2000;
  //connect to the socket server.
  //   var socket = io.connect("http://" + document.domain + ":" + location.port);
  var socket = io.connect();

  //receive details from server
  socket.on("updateSensorData", function (msg) {
    //console.log("Received sensorData: "+ msg.date + "::" + msg.metric + " :: " + msg.value);

    // Show only MAX_DATA_COUNT data
    if (eval(msg.metric).data.labels.length > MAX_DATA_COUNT) {
      removeFirstData(msg.metric);
    }
    addData(msg.date, msg.metric, msg.value);
    timeseries = ["outputHome","solarInput","outputPack"]
    if (timeseries.includes(msg.metric)) {
      updateCurValues(msg.metric, msg.value)
    }
  });

  socket.on("updateLimit", function(msg) {
    document.getElementById("state-" + msg.property).innerHTML = msg.value
  });
});
