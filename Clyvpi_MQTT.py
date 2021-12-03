import paho.mqtt.client as mqtt
import csv

import Clyvpi_DB
import ValueStorage

def write_to_csv_rfid_publish():
    with open('RFID_file.csv', mode='w') as csv_file:
        fieldnames = ['Parameter', 'Value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        rfid_value = ValueStorage.Scanned_RFID[2:-1]

        name = Clyvpi_DB.getUserByRfid(rfid_value)
        if name:
            print("GRANTED, Welcome " + name[0][0])
            client.publish("IoTlab/RFIDAccess", "GRANTED")
            writer.writeheader()
            writer.writerow({'Parameter': 'RFID', 'Value': f'{rfid_value}'})
            writer.writerow({'Parameter': 'Name', 'Value': f'{name[0][0]}'})
        #     Query the DB to receive the temp and light thresholds for that user.
            threshold_values = Clyvpi_DB.getThresoldByRfid(rfid_value)
            ValueStorage.Dash_Threshold_Light = threshold_values[0]
            ValueStorage.Dash_Threshold_Temp = threshold_values[1]
        #     Write the threshold values to the appropriate csv files.
            ValueStorage.write_to_csv_threshold_light()
            ValueStorage.write_to_csv_threshold_temp()


        else:
            print("DENIED")
            client.publish("IoTlab/RFIDAccess", "DENIED")
            writer.writeheader()
            writer.writerow({'Parameter': 'RFID', 'Value': f'{rfid_value}'})
            writer.writerow({'Parameter': 'Name', 'Value': f'Unknown'})




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

def read_from_csv_dash_publish_threshold_temp_light_LED():
    with open('Threshold_temp_LED_file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            print(
                f'\t{row["Parameter"]} has value {row["Value"]}')
            if row["Parameter"] == "Threshold_Temp_LED":
                ValueStorage.Dash_Threshold_Temp_LED = row["Value"]
    with open('Threshold_light_LED_file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            print(
                f'\t{row["Parameter"]} has value {row["Value"]}')
            if row["Parameter"] == "Threshold_Light_LED":
                ValueStorage.Dash_Threshold_Light_LED = row["Value"]

def read_from_csv_dash_publish_threshold_temp():
    with open('Threshold_temp_file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["Parameter"] == "Threshold_Temp":
                ValueStorage.Dash_Threshold_Temp = row["Value"]
                if ValueStorage.MQTT_temperature > float(ValueStorage.Dash_Threshold_Temp):
                    if ValueStorage.Dash_Threshold_Temp_LED != ValueStorage.Dash_Previous_Threshold_Temp_LED:
                        ValueStorage.Dash_Previous_Threshold_Temp_LED = ValueStorage.Dash_Threshold_Temp_LED
                        client.publish("IoTlab/ThresholdTemp", "ON")
                elif ValueStorage.MQTT_temperature < float(ValueStorage.Dash_Threshold_Temp):
                    if ValueStorage.Dash_Threshold_Temp_LED != ValueStorage.Dash_Previous_Threshold_Temp_LED:
                        ValueStorage.Dash_Previous_Threshold_Temp_LED = ValueStorage.Dash_Threshold_Temp_LED
                        client.publish("IoTlab/ThresholdTemp", "OFF")

def read_from_csv_dash_publish_threshold_light():
    final_string = ""
    with open('Threshold_light_file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if row["Parameter"] == "Threshold_Light":
                ValueStorage.Dash_Threshold_Light = row["Value"]
                if ValueStorage.MQTT_Light < float(ValueStorage.Dash_Threshold_Light):
                    if ValueStorage.Dash_Threshold_Light_LED != ValueStorage.Dash_Previous_Threshold_Light_LED:
                        ValueStorage.Dash_Previous_Threshold_Light_LED = ValueStorage.Dash_Threshold_Light_LED
                        client.publish("IoTlab/ThresholdLight", "ON")
                elif ValueStorage.MQTT_Light > float(ValueStorage.Dash_Threshold_Light):
                    if ValueStorage.Dash_Threshold_Light_LED != ValueStorage.Dash_Previous_Threshold_Light_LED:
                        ValueStorage.Dash_Previous_Threshold_Light_LED = ValueStorage.Dash_Threshold_Light_LED
                        client.publish("IoTlab/ThresholdLight", "OFF")


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("IoTlab/temperature")
    client.subscribe("IoTlab/humidity")
    client.subscribe("IoTlab/light")
    client.subscribe("IoTlab/tag")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    if msg.topic == "IoTlab/temperature":
        ValueStorage.MQTT_temperature = float(msg.payload)
        ValueStorage.Dash_Threshold_Temp = ValueStorage.read_from_csv_dash_threshold_temp()
        if ValueStorage.MQTT_temperature > float(ValueStorage.Dash_Threshold_Temp):
            ValueStorage.Dash_Threshold_Temp_LED = 'ON'
        else:
            ValueStorage.Dash_Threshold_Temp_LED = 'OFF'
        ValueStorage.write_to_csv_threshold_temp_LED()
    if msg.topic == "IoTlab/humidity":
        ValueStorage.MQTT_humidity = float(msg.payload)
    if msg.topic == "IoTlab/light":
        ValueStorage.MQTT_Light = float(msg.payload)
        ValueStorage.Dash_Threshold_Light = ValueStorage.read_from_csv_dash_threshold_light()
        if ValueStorage.MQTT_Light < int(ValueStorage.Dash_Threshold_Light):
            ValueStorage.Dash_Threshold_Light_LED = 'ON'
        else:
            ValueStorage.Dash_Threshold_Light_LED = 'OFF'
        ValueStorage.write_to_csv_threshold_light_LED()
        write_to_csv_MQTT()
        read_from_csv_dash_publish_LED()
        read_from_csv_dash_publish_Fan()
        read_from_csv_dash_publish_threshold_temp_light_LED()
        read_from_csv_dash_publish_threshold_temp()
        read_from_csv_dash_publish_threshold_light()

    if msg.topic == "IoTlab/tag":
        print("Got RFID...")
        ValueStorage.Scanned_RFID = str(msg.payload)
        write_to_csv_rfid_publish()

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

