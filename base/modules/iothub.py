from azure.iot.device import IoTHubDeviceClient
from azure.iot.hub import IoTHubRegistryManager
import os
import sys
import json
# from dotenv import load_dotenv

# load_dotenv()
# IOT_HUB_KEY = os.getenv('IOT_HUB_KEY')

# CONNECTION_STRING = IOT_HUB_KEY 
 
# CONNECTION_STRING = "HostName=iothubipd.azure-devices.net;DeviceId=raspberry;SharedAccessKey=ebnEBI2BTnGC9RkLtW7NqBsDV026Q7fDMAIoTCqCHuU="

def iothub_message(device_name, CONNECTION_STRING, status):
    try:
        registry_manager = IoTHubRegistryManager(CONNECTION_STRING)
        message_data = {
            "deviceId": device_name,
            "status": "off" if status else "on",
        }
        data = json.dumps(message_data)

        props = {
            "messageId": "message_1",
            "contentType": "application/json"
        }

        registry_manager.send_c2d_message("raspberry", data, properties=props)
        return True
    except Exception as e:
        print("Unexpected error:", e)
        return False
        

# def message_to_raspberrypi(device_name, CONNECTION_STRING, status):
#     # Create an instance of the device client using the connection string
#     client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
#     print(f"iothub: {CONNECTION_STRING}")
#     messages = [device_name, "off" if status else "on"]
#     message = " ".join(messages)
#     final_message = message.strip()
#     print(final_message)
#     # Send a message to the IoT Hub
#     try:
#         # Connect the client
#         client.connect()

#         # Send a message to the IoT Hub
#         print("Sending message: {}".format(final_message))
#         client.send_message(final_message)
#         client.disconnect()
#         return True

#     except Exception as e:
#         print("Unexpected error:", e)
#         return False

if __name__ == "__main__":
    message_to_raspberrypi("fan",False)