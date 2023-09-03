from zenapi import ZendureAPI as zapp
import json, time, logging, sys, os
from datetime import datetime
import time
from functools import reduce
from paho.mqtt import client as mqtt_client
from collections import namedtuple
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
from threading import Lock

FORMAT = '%(asctime)s:%(levelname)s: %(message)s'
logging.basicConfig(stream=sys.stdout, level="INFO", format=FORMAT)
log = logging.getLogger("")
logging.getLogger("urllib3").setLevel(logging.WARNING)
logging.getLogger("requests").setLevel(logging.WARNING)

ZEN_USER = os.environ.get('ZEN_USER',None)
ZEN_PASSWD = os.environ.get('ZEN_PASSWD',None)
MQTT_HOST = os.environ.get('MQTT_HOST',None)
MQTT_PORT = os.environ.get('MQTT_PORT',1883)

if ZEN_USER is None or ZEN_PASSWD is None:
    log.error("No username and password environment variable set (environment variable ZEN_USER, ZEN_PASSWD)!")
    sys.exit(0)

if MQTT_HOST is None:
    log.error("You need a local MQTT broker set (environment variable MQTT_HOST)!")
    sys.exit(0)

ZenAuth = namedtuple("ZenAuth",["productKey","deviceKey","clientId"])

# MQTT broker where we subscribe to all the telemetry data we need to steer
broker = 'mq.zen-iot.com'
port = 1883
client: mqtt_client

local_broker = MQTT_HOST
local_port = MQTT_PORT
local_client: mqtt_client
auth: ZenAuth
device_details = {}

# Flask SocketIO background task
thread = None
thread_lock = Lock()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

def on_solarflow_update(msg):
    global device_details
    global local_client
    payload = json.loads(msg)
    if "_properties_" in payload:
        log.info(payload["properties"])
        if "outputHomePower" in payload["properties"]:
            local_client.publish("solarflow-hub/telemetry/outputHomePower",payload["properties"]["outputHomePower"])
            socketio.emit('updateSensorData', {'metric': 'outputHome', 'value': payload["properties"]["outputHomePower"], 'date': round(time.time()*1000)})
        if "solarInputPower" in payload["properties"]:
            local_client.publish("solarflow-hub/telemetry/solarInputPower",payload["properties"]["solarInputPower"])
            socketio.emit('updateSensorData', {'metric': 'solarInput', 'value': payload["properties"]["solarInputPower"], 'date': round(time.time()*1000)})
        if "outputPackPower" in payload["properties"]:
            local_client.publish("solarflow-hub/telemetry/outputPackPower",payload["properties"]["outputPackPower"])
            socketio.emit('updateSensorData', {'metric': 'outputPack', 'value': -payload["properties"]["outputPackPower"], 'date': round(time.time()*1000)})
        if "packInputPower" in payload["properties"]:
            local_client.publish("solarflow-hub/telemetry/packInputPower",payload["properties"]["packInputPower"])
            socketio.emit('updateSensorData', {'metric': 'outputPack', 'value': payload["properties"]["packInputPower"], 'date': round(time.time()*1000)})
        if "electricLevel" in payload["properties"]:
            local_client.publish("solarflow-hub/telemetry/electricLevel",payload["properties"]["electricLevel"])
            socketio.emit('updateSensorData', {'metric': 'electricLevel', 'value': payload["properties"]["electricLevel"], 'date': round(time.time()*1000)})
            device_details["electricLevel"] = payload["properties"]["electricLevel"]
        if "outputLimit" in payload["properties"]:
            socketio.emit('updateLimit', {'property': 'outputLimit', 'value': f'{payload["properties"]["outputLimit"]} W'})
            device_details["outputLimit"] = payload["properties"]["outputLimit"]
        if "inputLimit" in payload["properties"]:
            socketio.emit('updateLimit', {'property': 'inputLimit', 'value': f'{payload["properties"]["inputLimit"]} W'})
            device_details["inputLimit"] = payload["properties"]["inputLimit"]
        if "socSet" in payload["properties"]:
            socketio.emit('updateLimit', {'property': 'socSet', 'value': f'{payload["properties"]["socSet"]/10} %'})
            device_details["socSet"] = payload["properties"]["socSet"]
        if "minSoc" in payload["properties"]:
            socketio.emit('updateLimit', {'property': 'minSoc', 'value': f'{payload["properties"]["minSoc"]/10} %'})
            device_details["minSoc"] = payload["properties"]["minSoc"]
            
    if "packData" in payload:
        log.info(payload["packData"])    
        if len(payload["packData"]) >= 1:
            for pack in payload["packData"]:
                if "socLevel" in pack:
                    socketio.emit('updateSensorData', {'metric': 'socLevel', 'value': pack["socLevel"], 'date': pack["sn"]})
                if "maxTemp" in pack:
                    socketio.emit('updateSensorData', {'metric': 'maxTemp', 'value': pack["maxTemp"]/100, 'date': pack["sn"]})
                if "minVol" in pack:
                    socketio.emit('updateSensorData', {'metric': 'minVol', 'value': pack["minVol"]/100, 'date': pack["sn"]})
                if "maxVol" in pack:
                    socketio.emit('updateSensorData', {'metric': 'maxVol', 'value': pack["maxVol"]/100, 'date': pack["sn"]})
                if "totalVol" in pack:
                    socketio.emit('updateSensorData', {'metric': 'totalVol', 'value': pack["totalVol"]/100, 'date': pack["sn"]})
                
            for dev_pack in device_details["packDataList"]:
                for pack in payload["packData"]:
                    if "socLevel" in pack:
                        if dev_pack["sn"] == pack["sn"]:
                            dev_pack["socLevel"] = pack["socLevel"]
                    if "maxTemp" in pack:
                        if dev_pack["sn"] == pack["sn"]:
                            dev_pack["maxTemp"] = pack["maxTemp"]


def on_local_message(client, userdata, msg):
    property = msg.topic.split('/')[-1]
    payload = msg.payload.decode()

    if "outputHomePower" == property:
        socketio.emit('updateSensorData', {'metric': 'outputHome', 'value': payload, 'date': round(time.time()*1000)})
    if "solarInputPower" == property:
        socketio.emit('updateSensorData', {'metric': 'solarInput', 'value': payload, 'date': round(time.time()*1000)})
    if "outputPackPower" == property:
        socketio.emit('updateSensorData', {'metric': 'outputPack', 'value': -payload, 'date': round(time.time()*1000)})
    if "packInputPower" == property:
        socketio.emit('updateSensorData', {'metric': 'outputPack', 'value': payload, 'date': round(time.time()*1000)})
    if "electricLevel" == property:
        socketio.emit('updateSensorData', {'metric': 'electricLevel', 'value': payload, 'date': round(time.time()*1000)})
        device_details["electricLevel"] = payload
    if "outputLimit" == property:
        socketio.emit('updateLimit', {'property': 'outputLimit', 'value': f'{payload} W'})
        device_details["outputLimit"] = payload
    if "inputLimit" == property:
        socketio.emit('updateLimit', {'property': 'inputLimit', 'value': f'{payload} W'})
        device_details["inputLimit"] = payload
    if "socSet" == property:
        socketio.emit('updateLimit', {'property': 'socSet', 'value': f'{payload/10} %'})
        device_details["socSet"] = payload
    if "minSoc" == property:
        socketio.emit('updateLimit', {'property': 'minSoc', 'value': f'{payload/10} %'})
        device_details["minSoc"] = payload


def on_message(client, userdata, msg):
    on_solarflow_update(msg.payload.decode())

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log.info("Connected to MQTT Broker!")
    else:
        log.error("Failed to connect, return code %d\n", rc)

def on_disconnect(client, userdata, rc):
    if rc != 0:
        log.warning("Unexpected disconnection.")
        mqtt_background_task()

def connect_mqtt(client_id) -> mqtt_client:
    global client
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username="zenApp", password="oK#PCgy6OZxd")
    client.reconnect_delay_set(min_delay=1, max_delay=120)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.connect(broker, port)
    return client

def connect_local_mqtt():
    global local_client
    global local_port
    local_client = mqtt_client.Client(client_id="solarflow-statuspage")
    local_client.reconnect_delay_set(min_delay=1, max_delay=120)
    local_client.on_connect = on_connect
    local_client.on_disconnect = on_disconnect
    local_client.connect(local_broker,local_port)
    return local_client

def subscribe(client: mqtt_client, auth: ZenAuth):
    # list of topics to subscribe
    report_topic = f'/{auth.productKey}/{auth.deviceKey}/properties/report'
    iot_topic = f'iot/{auth.productKey}/{auth.deviceKey}/#'
    client.subscribe(report_topic)
    client.subscribe(iot_topic)
    client.on_message = on_message

def subscribe_local(client: mqtt_client):
    telemetry_topic = "solarflow-hub/telemetry/#"
    client.subscribe(telemetry_topic)
    client.on_message = on_local_message

def get_auth() -> ZenAuth:
    global auth
    global device_details
    with zapp.ZendureAPI() as api:
        token = api.authenticate(ZEN_USER,ZEN_PASSWD)
        devices = api.get_device_ids()
        for dev_id in devices:
            device = api.get_device_details(dev_id)
            device_details = device
            auth = ZenAuth(device["productKey"],device["deviceKey"],token)

        log.info(f'Zendure Auth: {auth}')
        return auth

def mqtt_background_task():
    client = None
    #while client is None:
    try:
        auth = get_auth()
        #client = connect_mqtt(auth.clientId)
    except:
        log.warning("Connecting to MQTT broker failed!")
        time.sleep(10)

    #subscribe(client,auth)
    #client.loop_start()

def local_mqtt_background_task():
    client = None
    while client is None:
        try:
            client = connect_local_mqtt()
        except:
            log.warning("Connecting to local MQTT broker failed!")
            time.sleep(10)
    
    subscribe_local(client)
    client.loop_start()

@app.route('/')
def index():
    global devices
    return render_template('index.html', **device_details )

@socketio.on('connect')
def connect():
    global device_details
    log.info('Client connected')

    #emit device info we have collected on startup (may not be the full accurate data)
    socketio.emit('updateSensorData', {'metric': 'electricLevel', 'value': device_details["electricLevel"], 'date':  round(time.time()*1000)})

    for battery in device_details["packDataList"]:
        socketio.emit('updateSensorData', {'metric': 'socLevel', 'value': battery["socLevel"], 'date': battery["sn"]})
        socketio.emit('updateSensorData', {'metric': 'maxTemp', 'value': battery["maxTemp"]/10 if battery["maxTemp"] < 1000 else battery["maxTemp"]/100  , 'date': battery["sn"]})


@socketio.on('setLimit')
def setLimit(msg):
    global local_client
    
    jmsg = json.loads(msg)
    log.info(jmsg)
    payload = {"properties": { jmsg["property"]: int(jmsg["value"]) }}
    log.info(json.dumps(payload))
    local_client.publish(f'iot/{auth.productKey}/{auth.deviceKey}/properties/write', json.dumps(payload))

@socketio.on('disconnect')
def disconnect():
    log.info('Client disconnected')

if __name__ == '__main__':
    # starting mqtt network loop
    mqtt_background_task()

    # connect to local mqtt
    local_mqtt_background_task()
    
    socketio.run(app,host="0.0.0.0",allow_unsafe_werkzeug=True)
