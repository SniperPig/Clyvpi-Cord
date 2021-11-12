import paho.mqtt.client as mqtt
import csv
import ValueStorage

def write_to_csv_MQTT():
    with open('MQTT_file.csv', mode='w') as csv_file:
        fieldnames = ['Parameter', 'Value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Parameter': 'Temperature', 'Value': f'{ValueStorage.MQTT_temperature}'})
        writer.writerow({'Parameter': 'Humidity', 'Value': f'{ValueStorage.MQTT_humidity}'})
        writer.writerow({'Parameter': 'Light', 'Value': f'{ValueStorage.MQTT_Light}'})

def read_from_csv_dash_publish_LED():
    final_string = ""
    with open('Light_file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            print(
                f'\t{row["Parameter"]} has value {row["Value"]}')
            if row["Parameter"] == "Light":
                ValueStorage.Dash_Light = row["Value"]
                if ValueStorage.Dash_Light != ValueStorage.Dash_Previous_Light_Value:
                    ValueStorage.Dash_Previous_Light_Value = ValueStorage.Dash_Light
                    client.publish("IoTlab/LEDLight", str(ValueStorage.Dash_Light))
            line_count += 1

def read_from_csv_dash_publish_Fan():
    final_string = ""
    with open('Fan_file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            print(
                f'\t{row["Parameter"]} has value {row["Value"]}')
            if row["Parameter"] == "Fan":
                ValueStorage.Dash_Fan = row["Value"]
                if ValueStorage.Dash_Fan != ValueStorage.Dash_Previous_Fan_Value:
                    ValueStorage.Dash_Previous_Fan_Value = ValueStorage.Dash_Fan
                    client.publish("IoTlab/Fan", str(ValueStorage.Dash_Fan))
            line_count += 1

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("IoTlab/temperature")
    client.subscribe("IoTlab/humidity")
    client.subscribe("IoTlab/light")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "IoTlab/temperature":
        ValueStorage.MQTT_temperature = float(msg.payload)
    if msg.topic == "IoTlab/humidity":
        ValueStorage.MQTT_humidity = float(msg.payload)
    if msg.topic == "IoTlab/light":
        ValueStorage.MQTT_Light = float(msg.payload)
        write_to_csv_MQTT()
        read_from_csv_dash_publish_LED()
        read_from_csv_dash_publish_Fan()

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

