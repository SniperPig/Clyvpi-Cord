import csv

MQTT_temperature = ''
MQTT_humidity = ''
MQTT_Light = ''
Dash_Previous_Light_Value = ''
Dash_Fan = 'OFF'
Dash_Previous_Fan_Value = ''
Dash_Threshold_Light = ''
Dash_Threshold_Light_LED = ''
Dash_Previous_Threshold_Light_LED = ''
Dash_Threshold_Temp = ''
Dash_Threshold_Temp_LED = ''
Dash_Previous_Threshold_Temp_LED = ''
Send_Discord_Message = False
Dash_Previous_Threshold_LED_Value = ''

Scanned_RFID = ''


def read_from_csv_dash_threshold_temp():
    with open('Threshold_temp_file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            print(
                f'\t{row["Parameter"]} has value {row["Value"]}')
            if row["Parameter"] == "Threshold_Temp":
                return row["Value"]


def read_from_csv_dash_threshold_light():
    final_string = ""
    with open('Threshold_light_file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            print(
                f'\t{row["Parameter"]} has value {row["Value"]}')
            if row["Parameter"] == "Threshold_Light":
                return row["Value"]


def write_to_csv_threshold_light_LED():
    with open('Threshold_light_LED_file.csv', mode='w') as csv_file:
        fieldnames = ['Parameter', 'Value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Parameter': 'Threshold_Light_LED', 'Value': f'{Dash_Threshold_Light_LED}'})

def write_to_csv_threshold_temp_LED():
    with open('Threshold_temp_LED_file.csv', mode='w') as csv_file:
        fieldnames = ['Parameter', 'Value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Parameter': 'Threshold_Temp_LED', 'Value': f'{Dash_Threshold_Temp_LED}'})

def write_to_csv_threshold_light():
    with open('Threshold_light_file.csv', mode='w') as csv_file:
        fieldnames = ['Parameter', 'Value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Parameter': 'Threshold_Light', 'Value': f'{Dash_Threshold_Light}'})

def write_to_csv_threshold_temp():
    with open('Threshold_temp_file.csv', mode='w') as csv_file:
        fieldnames = ['Parameter', 'Value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Parameter': 'Threshold_Temp', 'Value': f'{Dash_Threshold_Temp}'})


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

