from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
import json
import math
import webview

webview.create_window("Gearbox", "http://localhost:5000/index.html")
webview.start()
app = Flask(__name__, static_url_path='', 
            static_folder='flaskr/static')


mph = 0
mode = "P"
gear = 1
maxGear = 7
gearInterval = 10
naturalFriction = 0.01
drivingModes = ["D", "R", "M"]

def setMode(newMode):
    global mode
    gear = 0
    if math.floor(mph) == 0:
        mode = newMode
        print("Set to gear " + newMode)
        return "success"
    else:
        return "not stationary"

@app.route("/set_d")
def set_d():
    return setMode("D")

@app.route("/set_r")
def set_r():
    return setMode("R")

@app.route("/set_p")
def set_p():
    return setMode("P")

@app.route("/set_m")
def set_m():
    return setMode("M")

@app.route("/gear_up")
def gear_up():
    global gear
    global maxGear
    if gear < maxGear and mph >= (gear*gearInterval-1) and mode == "M":
        gear += 1
        return "success"
    else:
        return "gear error"


@app.route("/gear_down")
def gear_down():
    global gear
    global maxGear
    if mode == "M" and gear > 1:
        gear -= 1
        return "success"
    else:
        return "gear cannot be below 1"  
    
@app.route("/get_info")
def get():
    content = {
                "mph" : math.floor(mph),
                "gear" : gear,
                "mode" : mode
            }
    print(json.dumps(content))
    return json.dumps(content) 

@app.route("/accelerate")
def acc():
    global mph
    if mode in drivingModes:
        mph += 1
        return "success"
    else:
        return "not in an acceptable gear"

@app.route("/brake")
def brake():
    global mph
    if mph > 1 and (mode in drivingModes):
        mph -= 1
        return "success"
    else:
        return "not in acceptable gear"

def simulate_gearbox():
    global mph
    global mode
    global gear
    global maxGear
    global gearInterval
    if mode == "D":
        gear = math.floor((mph-1)/gearInterval) + 1
        if gear <= 0:
            gear = 1
        if mph > (maxGear)*gearInterval:
            mph -= 1
        if mph >= naturalFriction:
            mph -= naturalFriction
    if mode == "R":
        gear = 1
        if mph > gearInterval:
            mph -= 1
        if mph >= naturalFriction:
            mph -= naturalFriction
    if mode == "M":
        print(gear*gearInterval)
        if mph > (gear)*gearInterval:
            mph -= 1
        if mph > naturalFriction:
            mph -= naturalFriction

scheduler = BackgroundScheduler()
scheduler.add_job(func=simulate_gearbox, trigger="interval", seconds=0.01)
scheduler.start()
