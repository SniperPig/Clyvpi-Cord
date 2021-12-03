import dash
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import dash_daq as daq
import csv
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import time
import ValueStorage
import bluetooth
import functools
from Clyvpi_Bluetooth import BluetoothRSSI


def read_from_csv_rfid():
    """
    Reads the RFID number from the RFID csv file.
    """
    with open('RFID_file.csv', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            print(
                f'\t{row["Parameter"]} has value {row["Value"]}')
            if row["Parameter"] == "RFID":
                ValueStorage.MQTT_RFID = row["Value"]
            if row["Parameter"] == "Name":
                ValueStorage.MQTT_RFID_Name = row["Value"]


# Initializing a Dash object which is the base UI layout of this program.
app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

# Initializing a Figure object that creates the temperature gauge.
temp_gauge_update = go.Figure(go.Indicator(
    mode="gauge+number",
    value=1,
    number={'suffix': " C°"},
    gauge={
        'axis': {'range': [-60, 60]},
        'bar': {'color': "black", 'thickness': 0.25},
        'borderwidth': 6,
        'bordercolor': "black",
        'steps': [
            {'range': [-60, 0], 'color': "blue"},
            {'range': [0, 40], 'color': "yellow"},
            {'range': [40, 60], 'color': "red"}
        ],
        'threshold': {'line': {'color': "black", 'width': 4},
                      'thickness': 0.75,
                      'value': 1}
    }
))

# Formatting the temperature gauge.
temp_gauge_update.update_layout(title="Temperature:", title_x=0.5, title_font_size=30, margin_b=55, margin_t=55,
                                margin_l=55, margin_r=55, paper_bgcolor="#0f0e12", height=330, font_size=20)

# Initializing a Figure object that creates the humidity gauge.
hum_gauge_update = go.Figure(go.Indicator(
    mode="gauge+number",
    value=1,
    number={'suffix': " %"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "black", 'thickness': 0.25},
        'borderwidth': 6,
        'bordercolor': "black",
        'steps': [
            {'range': [0, 33], 'color': "#b0ebff"},
            {'range': [33, 66], 'color': "#57d5ff"},
            {'range': [66, 100], 'color': "#00b2ee"}
        ],
        'threshold': {'line': {'color': "black", 'width': 4},
                      'thickness': 0.75,
                      'value': 1}
    }
))

# Formatting the humidity gauge.
hum_gauge_update.update_layout(title="Humidity:", title_x=0.5, title_font_size=30, margin_b=55, margin_t=55,
                               margin_l=55, margin_r=55, paper_bgcolor="#0f0e12", height=330, font_size=20)

# Initializing a Figure object that creates the light gauge.
light_gauge_update = go.Figure(go.Indicator(
    mode="gauge+number",
    value=1,
    number={'suffix': " %"},
    gauge={
        'axis': {'range': [0, 100]},
        'bar': {'color': "black", 'thickness': 0.25},
        'borderwidth': 6,
        'bordercolor': "black",
        'steps': [
            {'range': [0, 33], 'color': "#80A413"},
            {'range': [33, 66], 'color': "#C8FF00"},
            {'range': [66, 100], 'color': "#FFE800"}
        ],
        'threshold':
            {'line': {'color': "black", 'width': 4},
             'thickness': 0.75,
             'value': 1}
    }
))

# Formatting the light gauge.
light_gauge_update.update_layout(title="Light Intensity:", title_x=0.5, title_font_size=30, margin_b=55, margin_t=55,
                                 margin_l=55, margin_r=55, paper_bgcolor="#0f0e12", height=330, font_size=20)

# Initializes a variables which is responsible for scanning near by bluetooth devices.
devices = bluetooth.discover_devices(lookup_names=True)


def tuple_to_array(tup):
    """
    Converts a Tuple to an Array.
    :param tup: the desired tuple
    :type tup: tuple
    :return: an array
    :rtype: Array
    """
    arr = []
    for x in tup:
        arr.extend(x)
    return arr


def get_num_of_bluetooth_devices():
    """
    Gets the number of bluetooth devices.
    :return: the number of bluetooth devices
    :rtype: int
    """
    numOfDevices = 0
    for x in devices:
        numOfDevices += 1
    return numOfDevices


def get_bluetooth_devices_with_rssi():
    """
    Gets the name, mac address and RSSI of all detected bluetooth devices.
    :return: a list of all bluetooth devices
    :rtype: str
    """
    rssi_q_int = 0
    result = ''
    for x in devices:
        device = BluetoothRSSI(x[0])
        rssi_q = device.request_rssi()
        rssi_q_int = functools.reduce(lambda sub, ele: sub * 10 + ele, rssi_q)
        result += str(x)
        result += ' => RSSI: ' + str(rssi_q_int)

    return result


inputted_rssi_value = 0


def input_rssi_val(user_rssi_val):
    """
    Takes in an RSSI value and checks whether the value is greater than a certain number.
    :param user_rssi_val: the desired RSSI value to be checked
    :type user_rssi_val: int
    :return: all bluetooth devices that are greater than the inputted RSSI value
    :rtype: str
    """
    # rssi_devices = bluetooth.discover_devices(lookup_names=True)
    result = ''
    for x in devices:
        device = BluetoothRSSI(x[0])
        rssi_q = device.request_rssi()
        rssi_q_int = functools.reduce(lambda sub, ele: sub * 10 + ele, rssi_q)

        if (rssi_q_int < user_rssi_val):
            result += str(x)
            result += ' => RSSI: ' + str(rssi_q_int)

    return result


# Formatting the layout of the app using html.
app.layout = html.Div(style={'text-align': 'center', 'font-family': 'Candara'}, children=[
    html.B(html.P('Clyvpi Dashboard', style={'fontSize': 60, 'textAlign': 'center'})),
    html.Br(),
    read_from_csv_rfid(),
    html.Div(children=[
        html.H3('WELCOME, ' + f'{ValueStorage.MQTT_RFID_Name}'),
        html.H4('RFID#: ' + f'{ValueStorage.MQTT_RFID}'),
    ], style={'text-align': 'left'}),
    html.Br(),
    html.H5('Number of Bluetooth Devices: ' + str(get_num_of_bluetooth_devices())),
    html.H5(get_bluetooth_devices_with_rssi()),
    html.Br(),
    dcc.Graph(id='temp_gauge_update', figure=temp_gauge_update,
              style={'display': 'inline-block', 'width': '30%', 'border': "9px black double", 'border-radius': 5}),
    dcc.Graph(id='hum_gauge_update', figure=hum_gauge_update,
              style={'display': 'inline-block', 'width': '30%', 'border': "9px black double", 'border-radius': 5}),
    dcc.Graph(id='light_gauge_update', figure=light_gauge_update,
              style={'display': 'inline-block', 'width': '30%', 'border': "9px black double", 'border-radius': 5}),
    dcc.Interval(id='intervalComponent', interval=1 * 3000, n_intervals=0),
    html.Br(),
    html.Br(),
    html.Br(),

    # The input textbox for the temperature threshold.
    html.Div(children=[
        html.H4('Input Temperature Threshold:'),
        dcc.Input(
            id="TempTextBox",
            size='400',
            value=ValueStorage.read_from_csv_dash_threshold_temp(),
            type="number",
            placeholder="Temp Sensor Threshold",
            style={'width': '20%', 'height': 40, 'fontSize': 30}
        ),
    ], style={'display': 'inline-block'}),

    # The input textbox for the light threshold.
    html.Div(children=[
        html.H4('Input Light Threshold:'),
        dcc.Input(
            id="LightSensorTextBox",
            value=ValueStorage.read_from_csv_dash_threshold_light(),
            type="number",
            placeholder="Light Sensor Threshold",
            style={'width': '20%', 'height': 40, 'fontSize': 30}
        ),
    ], style={'display': 'inline-block'}),

    # The input textbox for the RSSI threshold.
    html.Div(children=[
        html.H4('RSSI Threshold:'),
        dcc.Input(
            id="RSSITextBox",
            value=0,
            type="number",
            placeholder="RSSI Threshold",
            style={'width': '20%', 'height': 40, 'fontSize': 30}
        ),
    ], style={'display': 'inline-block'}),

    html.Br(),
    html.Br(),
    html.H5(input_rssi_val(inputted_rssi_value)),
    html.Br(),
    html.H2('Turn LED ON/OFF'),

    # The switch for the LED.
    daq.ToggleSwitch(
        id='my-toggle-switch',
        value=False,
        size=90,
        color="#B5A5FF"
    ),
    html.Br(),
    html.Br(),
    html.Div(id='my-toggle-switch-output')
])


# Initializes a callback for the temperature gauge.
@app.callback([
    Output('temp_gauge_update', 'figure'), Output('hum_gauge_update', 'figure')], Output('light_gauge_update', 'figure'),
    [Input('intervalComponent', 'n_intervals')]
)
def update_gauges(n_intervals):
    """
    Updates the temperature value on the gauge after a certain amount of time (3000 milliseconds).
    :param n_intervals: amount of times the interval gets called
    :type n_intervals: int
    :return: the updated gauges
    :rtype: list
    """

    # The temperature value retrieved from the temperature csv file.
    temp_val_mqtt = float(ValueStorage.read_csv_MQTT_Temperature())
    # The humidity value retrieved from the humidity csv file.
    hum_val_mqtt = float(ValueStorage.read_csv_MQTT_Humidity())
    # The light value retrieved from the light csv file.
    light_mqtt = float(ValueStorage.read_csv_MQTT_Light())

    # The temperature gauge with the updated value.
    temp_gauge_update = go.Figure(go.Indicator(
        mode="gauge+number",
        value=temp_val_mqtt,
        number={'suffix': " C°"},
        gauge={
            'axis': {'range': [-60, 60]},
            'bar': {'color': "black", 'thickness': 0.25},
            'borderwidth': 6,
            'bordercolor': "black",
            'steps': [
                {'range': [-60, 0], 'color': "blue"},
                {'range': [0, 40], 'color': "yellow"},
                {'range': [40, 60], 'color': "red"}
            ],
            'threshold': {'line': {'color': "black", 'width': 4},
                          'thickness': 0.75,
                          'value': temp_val_mqtt}
        }
    ))

    # Formatting the temperature gauge.
    temp_gauge_update.update_layout(title="Temperature:", title_x=0.5, title_font_size=30, margin_b=55, margin_t=55,
                                  margin_l=55, margin_r=55, paper_bgcolor="#0f0e12", height=330, font_size=20)

    # The humidity gauge with the updated value.
    hum_gauge_update = go.Figure(go.Indicator(
        mode="gauge+number",
        value=hum_val_mqtt,
        number={'suffix': " %"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "black", 'thickness': 0.25},
            'borderwidth': 6,
            'bordercolor': "black",
            'steps': [
                {'range': [0, 33], 'color': "#b0ebff"},
                {'range': [33, 66], 'color': "#57d5ff"},
                {'range': [66, 100], 'color': "#00b2ee"}
            ],
            'threshold': {'line': {'color': "black", 'width': 4},
                          'thickness': 0.75,
                          'value': hum_val_mqtt}
        }
    ))

    # Formatting the humidity gauge.
    hum_gauge_update.update_layout(title="Humidity:", title_x=0.5, title_font_size=30, margin_b=55, margin_t=55,
                                 margin_l=55, margin_r=55, paper_bgcolor="#0f0e12", height=330, font_size=20)

    # The light gauge with the updated value.
    light_gauge_update = go.Figure(go.Indicator(
        mode="gauge+number",
        value=light_mqtt,
        number={'suffix': " %"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "black", 'thickness': 0.25},
            'borderwidth': 6,
            'bordercolor': "black",
            'steps': [
                {'range': [0, 33], 'color': "#80A413"},
                {'range': [33, 66], 'color': "#C8FF00"},
                {'range': [66, 100], 'color': "#FFE800"}
            ],
            'threshold':
                {'line': {'color': "black", 'width': 4},
                 'thickness': 0.75,
                 'value': light_mqtt}
        }
    ))

    # Formatting the light gauge.
    light_gauge_update.update_layout(title="Light Intensity:", title_x=0.5, title_font_size=30, margin_b=55, margin_t=55,
                                   margin_l=55, margin_r=55, paper_bgcolor="#0f0e12", height=330, font_size=20)

    return [temp_gauge_update, hum_gauge_update, light_gauge_update]


# Initializes a callback for the temperature textbox.
@app.callback(
    Output("TempTextBox", "value"), Input("TempTextBox", "value"))
def update_output(value):
    """
    Updates the temperature threshold textbox value
    :param value: temperature threshold textbox value
    :type value: int
    :return: the inputted value
    :rtype: int
    """
    time.sleep(3)
    ValueStorage.Dash_Threshold_Temp = value
    ValueStorage.write_to_csv_threshold_temp()
    return value


# Initializes a callback for the light textbox.
@app.callback(
    Output("LightSensorTextBox", "value"), Input("LightSensorTextBox", "value"))
def update_output(value):
    """
    Updates the light threshold textbox value.
    :param value: light threshold textbox value
    :type value: int
    :return: the inputted value
    :rtype: int
    """
    time.sleep(3)
    ValueStorage.Dash_Threshold_Light = value
    ValueStorage.write_to_csv_threshold_light()
    return value


# Initializes a callback for the RSSI textbox.
@app.callback(
    Output("RSSITextBox", "value"), Input("RSSITextBox", "value"))
def update_output(value):
    """
    Updates the RSSI threshold textbox value.
    :param value: RSSI threshold textbox value
    :type value: int
    :return: the inputted value
    :rtype: int
    """
    time.sleep(3)
    inputted_RSSI_value = value
    return value


# Initializes a callback for the LED toggle switch.
@app.callback(Output('my-toggle-switch-output', 'children'), Input('my-toggle-switch', 'value'))
def update_output(value):
    """
    Updates the LED threshold toggle switch value.
    :param value: LED threshold toggle switch value
    :return: the inputted value
    """
    if value == True:
        ret = "ON"
    elif value == False:
        ret = "OFF"
    ValueStorage.write_to_csv_light(ret)
    # return 'The switch is {}.'.format(value)


# Runs the app (through localhost).
if __name__ == '__main__':
    app.run_server(debug=True)
