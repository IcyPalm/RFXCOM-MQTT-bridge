import json
import logging
import sys

import paho.mqtt.client as mqtt
from RFXtrx import PySerialTransport, SensorEvent, ControlEvent, StatusEvent
from settings import *


loglevel = logging.getLevelName(LOGLEVEL)
logging.basicConfig(level=loglevel, filename="RFXlog.log")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.info("MQTT Connected with result code " + str(rc) + ": " + mqtt.connack_string(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PREFIX + "/#")
    mqtt_topic = MQTT_PREFIX + "/status"
    mqtt_client.publish(mqtt_topic, "Online!")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    # Does not do anything yet
    pass


transport = PySerialTransport(RFX_PORT, debug=RFX_DEBUG)

mqtt_client = mqtt.Client()  # Create the client
mqtt_client.on_connect = on_connect  # Callback on when connected
mqtt_client.on_message = on_message  # Callback when message received
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)  # Set user and pw
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)  # Connect the MQTT Client

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and aawa
# manual interface.
mqtt_client.loop_start()

while True:
    event = transport.receive_blocking()

    if event is None:
        continue

    logging.debug(event)
    if isinstance(event, SensorEvent):
        topic = MQTT_PREFIX + "/sensor/" + event.device.id_string
        json_payload = json.dumps(event.values)
        logging.info(topic + ": " + json_payload)
        mqtt_client.publish(topic, json_payload)

    if isinstance(event, ControlEvent):
        mqtt_topic = MQTT_PREFIX + "/control/" + event.device.id_string
        json_payload = json.dumps(event.values)
        logging.info(topic + ": " + json_payload)
        mqtt_client.publish(mqtt_topic, json_payload)

    if isinstance(event, StatusEvent):
        mqtt_topic = MQTT_PREFIX + "/status"
        logging.error("Statusevent: " + str(event))
        mqtt_client.publish(mqtt_topic, "StatusEvent received, cannot handle: " + str(event))

