from azure.iot.device import IoTHubDeviceClient
import os
# from dotenv import load_dotenv

# load_dotenv()
# IOT_HUB_KEY = os.getenv('IOT_HUB_KEY')

# CONNECTION_STRING = IOT_HUB_KEY

def message_to_raspberrypi(device_name, CONNECTION_STRING, status):
    # Create an instance of the device client using the connection string
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    print(f"iothub: {CONNECTION_STRING}")
    messages = [device_name, "off" if status else "on"]
    message = " ".join(messages)
    final_message = message.strip()
    print(final_message)
    # Send a message to the IoT Hub
    try:
        # Connect the client
        client.connect()

        # Send a message to the IoT Hub
        print("Sending message: {}".format(final_message))
        client.send_message(final_message)
        client.disconnect()
        return True

    except Exception as e:
        print("Unexpected error:", e)
        return False

if __name__ == "__main__":
    message_to_raspberrypi("fan",False)