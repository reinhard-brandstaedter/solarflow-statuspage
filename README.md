## Solarflow Statuspage and Control

The Solarflow Statuspage is an alternative to the mobile app. It gives a quick overview of the status of the hub, providing realtime data of the output to home, the current solar power generated and the battery charging power as well as the temperature nad individual battiers connected to your hub.
It also allows you manually to control the output to home and the battery charging limit.

<img src="img/solarflow_statuspage.png" width="250px" />

## How to use

I recommend to run the solarflow statuspage in a docker container to avoid any dependency issues.

You will need a Zendure Account. This is the login information you would also use with the Zendure Mobile App.

Pull the image with:
```
docker pull rbrandstaedter/solarflow-statuspage:latest
```

I recommend to create a ```.env``` file with your Zendure account credentials and load them as environment variables.
```
ZEN_USER=<your zendure account>
ZEN_PASSWD=<your zendure account password>
MQTT_HOST = <local mqtt host>
MQTT_PORT = <local mqtt port if different from default>
MQTT_USER = <mqtt user>
MQTT_PW = <mqtt user password>
```

Then run the container and expose it's port to a local port:
```
docker run -d --rm --env-file .env -p 127.0.0.1:5000:5000 --name solarflow-statuspage rbrandstaedter/solarflow-statuspage:latest
```

Open you browser and point it to [http://localhost:5000](http://localhost:5000)
You should see a page like above. After a few seconds you should see the charts populate with data.

## Notes
The Solarflow statuspage is not protected in any way. It is intended to run in a safe local-network environment and not meant to be exposed outside without any additional protection.