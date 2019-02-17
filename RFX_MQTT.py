import paho.mqtt.client as mqtt
from RFXtrx import PySerialTransport, SensorEvent
from settings import *


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc) + ": " + mqtt.connack_string(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(MQTT_PREFIX + "/#")


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


transport = PySerialTransport(RFX_PORT, debug=True)

mqtt_client = mqtt.Client()  # Create the client
mqtt_client.on_connect = on_connect  # Callback on when connected
mqtt_client.on_message = on_message  # Callback when message received
mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)  # Set user and pw
mqtt_client.connect(MQTT_HOST, MQTT_PORT, 60)  # Connect the MQTT Client

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
mqtt_client.loop_start()

while True:
    event = transport.receive_blocking()

    if event is None:
        continue

    print(event.values)
    if isinstance(event, SensorEvent):
        print(str(event.pkt.__class__.__name__))
    for value in event.values:
        topic = MQTT_PREFIX + "/" + str(event.device.type_string) + "/" + str(
            event.device.subtype) + "/" + event.device.id_string + "/" + value

        print(topic + " " + str(event.values[value]))
