async function getData(url) {
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Response status: ${response.status}`);
      }
  
      const json = await response.json();
      console.log(json);
      return json
    } catch (error) {
      console.error(error.message);
    }
  }

let winstreak = getData("/api/winstreak/"+shortid)
new Chart("winsteak", {
  type: "line",
  data: {
    labels: winstreak.x,
    datasets: [{
      backgroundColor:"rgba(0,0,255,1.0)",
      borderColor: "rgba(0,0,255,0.1)",
      data: winstreak.y
    }]
  },
  options: {
    legend: {display: false},
    scales: {
        yAxes: [{ticks: {min: 6, max:16}}],
        xAxes: [{type: 'time'}]
    }
}
});

let winrate = getData("/api/winrate/"+shortid)
new Chart("winrate", {
  type: "line",
  data: {
    labels: winrate.x,
    datasets: [{
      backgroundColor:"rgba(0,0,255,1.0)",
      borderColor: "rgba(0,0,255,0.1)",
      data: winrate.y
    }]
  },
  options: {
    legend: {display: false},
    scales: {
        yAxes: [{ticks: {min: 6, max:16}}],
        xAxes: [{type: 'time'}]
    }
}
});

let trophies = getData("/api/winstreak/"+shortid)
new Chart("trophies", {
  type: "line",
  data: {
    labels: trophies.x,
    datasets: [{
      backgroundColor:"rgba(0,0,255,1.0)",
      borderColor: "rgba(0,0,255,0.1)",
      data: trophies.y
    }]
  },
  options: {
    legend: {display: false},
    scales: {
        yAxes: [{ticks: {min: 6, max:16}}],
        xAxes: [{type: 'time'}]
    }
}
});