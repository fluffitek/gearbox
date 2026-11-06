var acel = false;
var brk = false;

const acelBtn = document.getElementById("acel")
const brkBtn = document.getElementById("brk")

const rqIfClick = {
  "r" : "/set_r",
  "d" : "/set_d",
  "m" : "/set_m",
  "p" : "/set_p",
  "ArrowUp" : "/gear_up",
  "ArrowDown" : "/gear_down"
}
function send(url)
{
    fetch(url)
    
    .then((response) => {
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    
    return response.text();
  })
}

function getUpdate()
{
    fetch("/get_info")
  .then((response) => {
    
    if (!response.ok) {
      throw new Error(`HTTP error: ${response.status}`);
    }
    return response.text()
  })
  .then(function(data) {
    parsedJSON = JSON.parse(data)
    
    document.getElementById("mph").innerHTML = parsedJSON.mph
    document.getElementById("mode").innerHTML = parsedJSON.mode
    document.getElementById("mphslider").value = parsedJSON.mph
    if (parsedJSON.gear == 1)
    {
      document.getElementById("gear").innerHTML = ""
    } 
    else
    {
      document.getElementById("gear").innerHTML = parsedJSON.gear
    } 
      var manual = (parsedJSON.mode == "M")

      if (manual)
      {
        document.getElementById("manual").classList.remove("hide")
      }
      else
      {
        document.getElementById("manual").classList.add("hide")
      }
    
  })
}

function acelCycle()
{
  if (acel == true)
  {
    send("/accelerate")
  }
  if (brk == true)
  {
    send("/brake")
  }
}

acelBtn.addEventListener("mousedown", () => {
  acel = true
})

acelBtn.addEventListener("mouseup", () => {
  acel = false
})

brkBtn.addEventListener("mousedown", () => {
  brk = true
})

brkBtn.addEventListener("mouseup", () => {
  brk = false
})

document.addEventListener("keydown", function (event) {
// Then display the event.key
  if (event.repeat) {
    return
  }
  console.log("You pressed: " + event.key)
  if (rqIfClick[event.key] != null)
  {
    send(rqIfClick[event.key])
    console.log(rqIfClick[event.key])
  }
  
  if (event.key == "w")
  {
    acel = true
  }
  else if (event.key == "s")
  {
    brk = true
  }
});

document.addEventListener("keyup", function (event) {
  if (event.key == "w")
  {
    acel = false
  }
  if (event.key == "s")
  {
    brk = false
  }
})
getUpdate()
setInterval(getUpdate, 50);
setInterval(acelCycle, 150)