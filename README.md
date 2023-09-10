## Solarflow Statuspage and Control

The Solarflow Statuspage is an alternative to the mobile app. It gives a quick overview of the status of the hub, providing realtime data of the output to home, the current solar power generated and the battery charging power as well as the temperature nad individual battiers connected to your hub.
It also allows you manually to control the output to home and the battery charging/discahrgin limits.
Additionally the statuspage can push the data it reads from Zendure's cloud service to a local MQTT broker so that you can use it for further processing (e.g. homeautomation integration).

<img src="/img/statuspage.png" width="250px" />


## How to use

I recommend to run the solarflow statuspage in a docker container to avoid any dependency issues.

You will need a Zendure Account. This is the login information you would also use with the Zendure Mobile App.

### Online/Offline mode
The statuspage has two ways to aquire the hubs telemetry data: online/offline.
In *online* mode it will connect to Zendure's Cloud MQTT to retrieve the telemtry data. You will need to provide your Zendure credentials (```ZEN_USER``` and ```ZEN_PASSWD``) as environment variables.
In *offline* mode it expects the telemetry data already reported (and transformed) in your local MQTT. This is an advanced usecase where you'll need to take you hub offline first (see [solarflow-bt-manager](https://github.com/reinhard-brandstaedter/solarflow-bt-manager) how to achieve this) 

### Run in Docker

Pull the image with:
```
docker pull rbrandstaedter/solarflow-statuspage:master
```

I recommend to create a ```.env``` file in the directory where you will start the container. This file should contain your Zendure account credentials and other environment variables needed.
```
ZEN_USER=<your zendure account>
ZEN_PASSWD=<your zendure account password>
MQTT_HOST = <local mqtt host>
MQTT_PORT = <local mqtt port if different from default>
MQTT_USER = <mqtt user>
MQTT_PWD = <mqtt user password>
```

Then run the container and expose it's port to a local port. Make sure to also specify the --online option, as per default the statuspage will try to work ```offline``` (meaning it will expect the telemetry data already in MQTT, provided by an offline hub) 
```
docker run --rm --env-file .env -p 127.0.0.1:5000:5000 --name solarflow-statuspage rbrandstaedter/solarflow-statuspage:master --online
```

Open you browser and point it to [http://localhost:5000](http://localhost:5000)
You should see a page like above. After a few seconds you should see the charts populate with data.

### Run without Docker

Of course you can also run the statuspage without Docker on any OS with appropriate python3 installed. First clone the repository (or manually copy the source from github).

```
# git clone https://github.com/reinhard-brandstaedter/solarflow-statuspage.git
```

Install the dependencies (assuming you already have python3)
```
# cd solarflow-stauspage/src
# pip install -r requirements.txt
```

Set the required environment variables:
```
# export ZEN_USER=<your zendure account>
# export ZEN_PASSWD=<your zendure account password>
# export MQTT_HOST = <local mqtt host> 
# export MQTT_PORT = <local mqtt port>
# export MQTT_USER = <mqtt user> (optional)
# export MQTT_PWD = <mqtt user password> (optional)
```

Start the statuspage
```
# python3 solarflow-status.py --online
```

## Notes
The Solarflow statuspage is not protected in any way. It is intended to run in a safe local-network environment and not meant to be exposed outside without any additional protection.
