import csv

MQTT_temperature = ''
MQTT_humidity = ''
MQTT_Light = ''
Dash_Previous_Light_Value = ''
Dash_Fan = 'OFF'
Dash_Previous_Fan_Value = ''
Dash_Threshold_Light = 15
Dash_Threshold_Light = 15
Dash_Threshold_LED = 'OFF'
Send_Discord_Message = False
Dash_Previous_Threshold_LED_Value = ''

Scanned_RFID = ''


def write_to_csv_light(value):
    with open('Light_file.csv', mode='w') as csv_file:
        fieldnames = ['Parameter', 'Value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Parameter': 'Light', 'Value': f'{value}'})


def write_to_csv_fan(value):
    with open('Fan_file.csv', mode='w') as csv_file:
        fieldnames = ['Parameter', 'Value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Parameter': 'Fan', 'Value': f'{value}'})


def read_csv_MQTT():
    final_string = ""
    with open('MQTT_file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            print(
                f'\t{row["Parameter"]} has value {row["Value"]}')
            if row["Parameter"] == "Temperature":
                final_string += f'**{row["Parameter"]}** : {row["Value"]}' + u'\N{DEGREE SIGN}C' + '\n'
            if row["Parameter"] == "Humidity":
                final_string += f'**{row["Parameter"]}** : {row["Value"]}%\n'
            if row["Parameter"] == "Light":
                final_string += f'**{row["Parameter"]}** : {row["Value"]}%\n'
            line_count += 1
        print(f'Processed {line_count} lines.')
        return final_string


def read_from_csv_light():
    final_string = ""
    with open('Light_file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            print(
                f'\t{row["Parameter"]} is {row["Value"]}')
            final_string += f'**{row["Parameter"]}** is {row["Value"]}'
            line_count += 1
        print(f'Processed {line_count} lines.')
        return final_string


def read_from_csv_fan():
    final_string = ""
    with open('Fan_file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            print(
                f'\t{row["Parameter"]} is {row["Value"]}')
            final_string += f'**{row["Parameter"]}** is {row["Value"]}'
            line_count += 1
        print(f'Processed {line_count} lines.')
        return final_string


def write_to_csv_light_threshold(value):
    with open('Light_file.csv', mode='w') as csv_file:
        fieldnames = ['Parameter', 'Value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Parameter': 'LightThreshold', 'Value': f'{value}'})


def read_csv_MQTT_Temperature():
    final_string = ""
    with open('MQTT_file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if row["Parameter"] == "Temperature":
                return row["Value"]


def read_csv_MQTT_Humidity():
    final_string = ""
    with open('MQTT_file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if row["Parameter"] == "Humidity":
                return row["Value"]


def read_csv_MQTT_Light():
    final_string = ""
    with open('MQTT_file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if row["Parameter"] == "Light":
                return row["Value"]

