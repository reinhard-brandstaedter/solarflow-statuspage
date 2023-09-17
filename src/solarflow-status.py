from zenapi import ZendureAPI as zapp
import json, time, logging, sys, os
from datetime import datetime
import time
from paho.mqtt import client as mqtt_client
from collections import namedtuple
from flask import Flask, render_template
from flask_socketio import SocketIO
import random
from threading import Lock
import click

FORMAT = '%(asctime)s:%(levelname)s: %(message)s'
logging.basicConfig(stream=sys.stdout, level="INFO", format=FORMAT)
log = logging.getLogger("")

ZEN_USER = os.environ.get('ZEN_USER',None)
ZEN_PASSWD = os.environ.get('ZEN_PASSWD',None)
MQTT_HOST = os.environ.get('MQTT_HOST',None)
MQTT_PORT = int(os.environ.get('MQTT_PORT',1883))
MQTT_USER = os.environ.get('MQTT_USER',None)
MQTT_PW = os.environ.get('MQTT_PWD',None)


if MQTT_HOST is None:
    log.error("You need a local MQTT broker set (environment variable MQTT_HOST)!")
    sys.exit(0)

ZenAuth = namedtuple("ZenAuth",["productKey","deviceKey","clientId"])

# MQTT broker where we subscribe to all the telemetry data we need to steer
broker = 'mq.zen-iot.com'
port = 1883
zendure_client: mqtt_client

local_broker = MQTT_HOST
local_port = MQTT_PORT
local_client: mqtt_client
offline_mode: bool
auth: ZenAuth
device_details = {"productName": "n/a", "snNumber": "n/a", "wifiName": "n/a", "wifiState": "n/a", "ip": "n/a", "packNum": "0", "socSet": 0, "minSoc": 0, "inverseMaxPower":0, "outputLimit":0}

# Flask SocketIO background task
thread = None
thread_lock = Lock()

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')

def get_current_datetime():
    now = datetime.now()
    return now.strftime("%H:%M:%S")

def softVersion(version: int):
    major = (version & 0xf000) >> 12
    minor = (version & 0x0f00) >> 8
    build = (version & 0x00ff)
    return f'{major}.{minor}.{build}'

def on_zendure_message(client, userdata, msg):
    global device_details
    global local_client
    payload = json.loads(msg.payload.decode())
    if "properties/report" in msg.topic and "properties" in payload:
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
        if "socSet" in payload["properties"]:
            socketio.emit('updateLimit', {'property': 'socSet', 'value': f'{payload["properties"]["socSet"]/10} %'})
            device_details["socSet"] = payload["properties"]["socSet"]
        if "minSoc" in payload["properties"]:
            socketio.emit('updateLimit', {'property': 'minSoc', 'value': f'{payload["properties"]["minSoc"]/10} %'})
            device_details["minSoc"] = payload["properties"]["minSoc"]
        if "inverseMaxPower" in payload["properties"]:
            socketio.emit('updateLimit', {'property': 'inverseMaxPower', 'value': f'{payload} W'})
            device_details["inverseMaxPower"] = payload["properties"]["inverseMaxPower"]
            
    if "packData" in payload:
        log.info(payload["packData"])    
        if len(payload["packData"]) >= 1:
            for pack in payload["packData"]:
                if "socLevel" in pack:
                    local_client.publish(f'solarflow-hub/telemetry/batteries/{pack["sn"]}/socLevel',pack["socLevel"])
                    socketio.emit('updateSensorData', {'metric': 'socLevel', 'value': pack["socLevel"], 'date': pack["sn"]})
                if "maxTemp" in pack:
                    local_client.publish(f'solarflow-hub/telemetry/batteries/{pack["sn"]}/maxTemp',pack["maxTemp"])
                    socketio.emit('updateSensorData', {'metric': 'maxTemp', 'value': pack["maxTemp"]/100, 'date': pack["sn"]})
                if "minVol" in pack:
                    local_client.publish(f'solarflow-hub/telemetry/batteries/{pack["sn"]}/minVol',pack["minVol"])
                    socketio.emit('updateSensorData', {'metric': 'minVol', 'value': pack["minVol"]/100, 'date': pack["sn"]})
                if "maxVol" in pack:
                    local_client.publish(f'solarflow-hub/telemetry/batteries/{pack["sn"]}/maxVol',pack["maxVol"])
                    socketio.emit('updateSensorData', {'metric': 'maxVol', 'value': pack["maxVol"]/100, 'date': pack["sn"]})
                if "totalVol" in pack:
                    local_client.publish(f'solarflow-hub/telemetry/batteries/{pack["sn"]}/totalVol',pack["totalVol"])
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
    global device_details
    property = msg.topic.split('/')[-1]
    payload = msg.payload.decode()

    # determine deviceID and productID
    if "properties/report" in msg.topic:
        parts = msg.topic.split('/')
        device_details["productKey"] = parts[1]
        device_details["deviceKey"] = parts[2]

    # determine serial number from log messages
    if "log" in msg.topic:
        payload = json.loads(payload)
        if "log" in payload:
            #device_details["snNumber"] = payload["log"]["sn"]
            socketio.emit('updateLimit', {'property': 'snNumber', 'value': f'{payload["log"]["sn"]}'})

    # act as a forwarder for write commands on local MQTT
    if "properties/write" in msg.topic:
        if not offline_mode:
            log.info("Online mode: forwarding limit command to Zendure Cloud")
            set_zendure_limit(payload)

    if "batteries" in msg.topic:
        sn = msg.topic.split('/')[-2]
        if property not in  ["socLevel", "power"]:
            payload = float(payload)/100

        if property in ["minVol", "maxVol", "maxTemp", "totalVol", "socLevel"]:
            socketio.emit('updateSensorData', {'metric': property, 'value': payload, 'date': sn})
        if property in ["power"]:
            socketio.emit('updateSensorData', {'metric': "batteryPower", 'value': payload, 'sn': sn, 'date': round(time.time()*1000)})

    elif "solarflow-hub" in msg.topic:
        try:
            payload = int(payload)
        except:
            log.error(f'Error converting payload to int: {payload}')

        if "outputHomePower" == property:
            socketio.emit('updateSensorData', {'metric': 'outputHome', 'value': int(payload), 'date': round(time.time()*1000)})
        if "solarInputPower" == property:
            socketio.emit('updateSensorData', {'metric': 'solarInput', 'value': int(payload), 'date': round(time.time()*1000)})
        if "outputPackPower" == property:
            socketio.emit('updateSensorData', {'metric': 'outputPack', 'value': -int(payload), 'date': round(time.time()*1000)})
        if "packInputPower" == property:
            socketio.emit('updateSensorData', {'metric': 'outputPack', 'value': int(payload), 'date': round(time.time()*1000)})
        if "electricLevel" == property:
            socketio.emit('updateSensorData', {'metric': 'electricLevel', 'value': int(payload), 'date': round(time.time()*1000)})
            device_details["electricLevel"] = payload
        if "homeUsage" == property:
            socketio.emit('updateSensorData', {'metric': 'homeUsage', 'value': int(payload), 'date': round(time.time()*1000)})
        if "outputLimit" == property:
            socketio.emit('updateLimit', {'property': 'outputLimit', 'value': f'{payload} W'})
            device_details["outputLimit"] = payload
        if "socSet" == property:
            socketio.emit('updateLimit', {'property': 'socSet', 'value': f'{payload/10} %'})
            device_details["socSet"] = payload
        if "minSoc" == property:
            socketio.emit('updateLimit', {'property': 'minSoc', 'value': f'{payload/10} %'})
            device_details["minSoc"] = payload
        if "inverseMaxPower" == property:
            socketio.emit('updateLimit', {'property': 'inverseMaxPower', 'value': f'{payload} W'})
            device_details["inverseMaxPower"] = payload
        if "packNum" == property:
            socketio.emit('updateLimit', {'property': 'packNum', 'value': f'{payload}'})
            device_details["packNum"] = payload
        if "wifiState" == property:
            socketio.emit('updateLimit', {'property': 'wifiState', 'value': f'{bool(int(payload))}'})
            device_details["wifiState"] = payload
        if "masterSoftVersion" == property:
            socketio.emit('updateLimit', {'property': 'masterSoftVersion', 'value': softVersion(payload)})
            device_details["masterSoftVersion"] = payload



def on_connect(client, userdata, flags, rc):
    if rc == 0:
        log.info(f'Connected to MQTT Broker: {userdata}')
    else:
        log.error("Failed to connect, return code %d\n", rc)

def on_zendure_disconnect(client, userdata, rc):
    if rc != 0:
        log.warning("Unexpected disconnection.")
        zendure_mqtt_background_task()

def on_local_disconnect(client, userdata, rc):
    if rc != 0:
        log.warning("Unexpected disconnection.")
        local_mqtt_background_task()

def connect_zendure_mqtt(client_id) -> mqtt_client:
    global zendure_client
    zendure_client = mqtt_client.Client(client_id=client_id, userdata="Zendure Production MQTT")
    zendure_client.username_pw_set(username="zenApp", password="oK#PCgy6OZxd")
    zendure_client.reconnect_delay_set(min_delay=1, max_delay=120)
    zendure_client.on_connect = on_connect
    zendure_client.on_disconnect = on_zendure_disconnect
    zendure_client.connect(broker, port)
    return zendure_client

def connect_local_mqtt(client_id) -> mqtt_client:
    global local_client
    global local_port
    log.info(f'Connecting to MQTT with: {client_id}')
    local_client = mqtt_client.Client(client_id=client_id, userdata=f'Local MQTT ({local_broker}:{local_port})')
    if MQTT_USER is not None and MQTT_PW is not None:
        local_client.username_pw_set(MQTT_USER, MQTT_PW)
    local_client.reconnect_delay_set(min_delay=1, max_delay=120)
    local_client.on_connect = on_connect
    local_client.on_disconnect = on_local_disconnect
    local_client.connect(local_broker,local_port)
    return local_client

def zendure_subscribe(client: mqtt_client, auth: ZenAuth):
    report_topic = f'/{auth.productKey}/{auth.deviceKey}/properties/report'
    iot_topic = f'iot/{auth.productKey}/{auth.deviceKey}/#'
    client.subscribe(report_topic)
    client.subscribe(iot_topic)
    client.on_message = on_zendure_message

def local_subscribe(client: mqtt_client):
    log.info(f'Subscribing to topics...')
    client.subscribe( "solarflow-hub/telemetry/#")
    client.subscribe("solarflow-hub/control/#")
    client.subscribe("/73bkTV/+/properties/report")
    client.subscribe("/73bkTV/+/log")
    client.subscribe("iot/73bkTV/+/properties/write")
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

def zendure_mqtt_background_task():
    client = None
    while client is None:
        try:
            auth = get_auth()
            client = connect_zendure_mqtt(auth.clientId)
        except:
            log.exception("Connecting to Zendure's MQTT broker failed!")
            sys.exit(0)

    zendure_subscribe(client,auth)
    client.loop_start()

def local_mqtt_background_task():
    client = None
    while client is None:
        try:
            log.info(f'Connectiong local MQTT: {local_broker}:{local_port}')
            client_id = f'solarflow-statuspage-{random.randint(0, 100)}'
            client = connect_local_mqtt(client_id)
        except:
            log.exception("Connecting to local MQTT broker failed!")
            time.sleep(10)
    
    local_subscribe(client)
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
    if "electricLevel" in device_details:
        socketio.emit('updateSensorData', {'metric': 'electricLevel', 'value': device_details["electricLevel"], 'date':  round(time.time()*1000)})

    if "packDataList" in device_details:
        for battery in device_details["packDataList"]:
            socketio.emit('updateSensorData', {'metric': 'socLevel', 'value': battery["socLevel"], 'date': battery["sn"]})
            socketio.emit('updateSensorData', {'metric': 'maxTemp', 'value': battery["maxTemp"]/10 if battery["maxTemp"] < 1000 else battery["maxTemp"]/100  , 'date': battery["sn"]})

def set_local_limit(payload):
    global local_client
    local_client.publish(f'iot/{device_details["productKey"]}/{device_details["deviceKey"]}/properties/write', payload)
    log.info(f'Publishing offline limit command: {payload}')

def set_zendure_limit(payload):
    global zendure_client
    zendure_client.publish(f'iot/{device_details["productKey"]}/{device_details["deviceKey"]}/properties/write', payload)
    log.info(f'Publishing online limit command: {payload}')

@socketio.on('setLimit')
def setLimit(msg):
    jmsg = json.loads(msg)
    payload = {"properties": { jmsg["property"]: int(jmsg["value"]) }}
    log.info(json.dumps(payload))
    if offline_mode:
        set_local_limit(json.dumps(payload))
    else:
        set_zendure_limit(json.dumps(payload))

@socketio.on('disconnect')
def disconnect():
    log.info('Client disconnected')

@click.command()
@click.option("--offline/--online", default=True, help="Online/Offline mode: either connect to the Zendure API/MQTT or not (requires local MQTT with hub data present)")
#@click.option("--online", default=False, help="Work in online mode, connecting to the Zendure API (requires User/Pwd) and to Zendures MQTT to get data")
def setup(offline):
    global offline_mode
    offline_mode = offline
    if offline:
        # connect to local mqtt
        local_mqtt_background_task()
    else:
        if ZEN_USER is None or ZEN_PASSWD is None:
            log.error("No username and password environment variable set (environment variable ZEN_USER, ZEN_PASSWD)!")
            sys.exit(0)

        # connect to zendure mqtt
        zendure_mqtt_background_task()

        # connect to local mqtt
        local_mqtt_background_task()

        

    socketio.run(app,host="0.0.0.0",allow_unsafe_werkzeug=True)

if __name__ == '__main__':
    setup()
