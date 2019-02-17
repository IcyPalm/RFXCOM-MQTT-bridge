import os
from dotenv import load_dotenv

load_dotenv()

MQTT_PREFIX = os.getenv("MQTT_PREFIX")
MQTT_HOST = os.getenv("MQTT_HOST")
MQTT_PORT = int(os.getenv("MQTT_PORT"))
MQTT_USER = os.getenv("MQTT_USER")
MQTT_PASS = os.getenv("MQTT_PASS")
RFX_PORT = os.getenv("RFX_PORT")
