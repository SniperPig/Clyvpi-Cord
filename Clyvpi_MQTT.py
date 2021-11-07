import paho.mqtt.client as mqtt
import csv
import ValueStorage

def write_to_csv():
    with open('MQTT_file.csv', mode='w') as csv_file:
        fieldnames = ['Parameter', 'Value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Parameter': 'Temperature', 'Value': f'{ValueStorage.MQTT_temperature}'})
        writer.writerow({'Parameter': 'Humidity', 'Value': f'{ValueStorage.MQTT_humidity}'})
# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("IoTlab/temperature")
    client.subscribe("IoTlab/humidity")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "IoTlab/temperature":
        ValueStorage.MQTT_temperature = float(msg.payload)
    if msg.topic == "IoTlab/humidity":
        ValueStorage.MQTT_humidity = float(msg.payload)

        write_to_csv()

def on_publish(client,userdata,result):             #create function for callback
    print("data published \n")
    pass

client = mqtt.Client()
client.on_publish = on_publish
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.100", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

