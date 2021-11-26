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

inputted_RSSI_value = 0

app = dash.Dash(external_stylesheets=[dbc.themes.DARKLY])

tempGaugeUpdate = go.Figure(go.Indicator(
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
tempGaugeUpdate.update_layout(title="Temperature:", title_x=0.5, title_font_size=30, margin_b=55, margin_t=55,
                              margin_l=55, margin_r=55, paper_bgcolor="#0f0e12", height=330, font_size=20)

humGaugeUpdate = go.Figure(go.Indicator(
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
humGaugeUpdate.update_layout(title="Humidity:", title_x=0.5, title_font_size=30, margin_b=55, margin_t=55,
                             margin_l=55, margin_r=55, paper_bgcolor="#0f0e12", height=330, font_size=20)

lightGaugeUpdate = go.Figure(go.Indicator(
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
lightGaugeUpdate.update_layout(title="Light Intensity:", title_x=0.5, title_font_size=30, margin_b=55, margin_t=55,
                               margin_l=55, margin_r=55, paper_bgcolor="#0f0e12", height=330, font_size=20)

devices = bluetooth.discover_devices(lookup_names=True)

def tupleToArray(tup):
    arr = []
    for x in tup:
        arr.extend(x)
    return arr

def getNumOfBluetoothDevice():
    numOfDevices = 0
    for x in devices:
        numOfDevices += 1
    return numOfDevices

def getBluetoothDevicesWithRSSI():
    rssi_q_int = 0
    result = ''
    for x in devices:
        device = BluetoothRSSI(x[0])
        rssi_q = device.request_rssi()
        rssi_q_int = functools.reduce(lambda sub, ele: sub * 10 + ele, rssi_q)
        result += str(x)
        result += ' => RSSI: ' + str(rssi_q_int)

    return result

def inputRSSIVal(user_rssi_val):
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

app.layout = html.Div(style={'text-align': 'center', 'font-family': 'Candara'}, children=[
    html.B(html.P('Clyvpi Dashboard', style={'fontSize': 60, 'textAlign': 'center'})),
    html.Br(),
    html.Div(children=[
        html.H3('WELCOME, SussyBaka.'),
        html.H4('RFID#: 4206942069'),
    ], style={'text-align': 'left'}),
    html.Br(),
    html.H5('Number of Bluetooth Devices: ' + str(getNumOfBluetoothDevice())),
    html.H5(getBluetoothDevicesWithRSSI()),
    html.Br(),
    dcc.Graph(id='tempGaugeUpdate', figure=tempGaugeUpdate, style={'display': 'inline-block', 'width': '30%', 'border': "9px black double", 'border-radius': 5}),
    dcc.Graph(id='humGaugeUpdate', figure=humGaugeUpdate, style={'display': 'inline-block', 'width': '30%', 'border': "9px black double", 'border-radius': 5}),
    dcc.Graph(id='lightGaugeUpdate', figure=lightGaugeUpdate, style={'display': 'inline-block', 'width': '30%', 'border': "9px black double", 'border-radius': 5}),
    dcc.Interval(id='intervalComponent', interval=1 * 3000, n_intervals=0),
    html.Br(),
    html.Br(),
    html.Br(),

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
    html.H5(inputRSSIVal(inputted_RSSI_value)),
    html.Br(),
    html.H2('Turn LED ON/OFF'),
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

@app.callback([
    Output('tempGaugeUpdate', 'figure'), Output('humGaugeUpdate', 'figure')], Output('lightGaugeUpdate', 'figure'),
    [Input('intervalComponent', 'n_intervals')]
)
def update_temp_gauge(n_intervals):
    tempValMQTT = float(ValueStorage.read_csv_MQTT_Temperature())
    humValMQTT = float(ValueStorage.read_csv_MQTT_Humidity())
    lightMQTT = float(ValueStorage.read_csv_MQTT_Light())
    tempGaugeUpdate = go.Figure(go.Indicator(
        mode="gauge+number",
        value=tempValMQTT,
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
                          'value': tempValMQTT}
        }
    ))
    tempGaugeUpdate.update_layout(title="Temperature:", title_x=0.5, title_font_size=30, margin_b=55, margin_t=55,
                                  margin_l=55, margin_r=55, paper_bgcolor="#0f0e12", height=330, font_size=20)

    humGaugeUpdate = go.Figure(go.Indicator(
        mode="gauge+number",
        value=humValMQTT,
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
                          'value': humValMQTT}
        }

    ))
    humGaugeUpdate.update_layout(title="Humidity:", title_x=0.5, title_font_size=30, margin_b=55, margin_t=55,
                                 margin_l=55, margin_r=55, paper_bgcolor="#0f0e12", height=330, font_size=20)

    lightGaugeUpdate = go.Figure(go.Indicator(
        mode="gauge+number",
        value=lightMQTT,
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
                 'value': lightMQTT}
        }
    ))
    lightGaugeUpdate.update_layout(title="Light Intensity:", title_x=0.5, title_font_size=30, margin_b=55, margin_t=55,
                                   margin_l=55, margin_r=55, paper_bgcolor="#0f0e12", height=330, font_size=20)

    return [tempGaugeUpdate, humGaugeUpdate, lightGaugeUpdate]


@app.callback(
    Output("TempTextBox", "value"), Input("TempTextBox", "value"))
def update_output(value):
    time.sleep(3)
    ValueStorage.Dash_Threshold_Temp = value
    ValueStorage.write_to_csv_threshold_temp()
    return value


@app.callback(
    Output("LightSensorTextBox", "value"), Input("LightSensorTextBox", "value"))
def update_output(value):
    time.sleep(3)
    ValueStorage.Dash_Threshold_Light = value
    ValueStorage.write_to_csv_threshold_light()
    return value

@app.callback(
    Output("RSSITextBox", "value"), Input("RSSITextBox", "value"))
def update_output(value):
    time.sleep(3)
    inputted_RSSI_value = value
    return value


@app.callback(Output('my-toggle-switch-output', 'children'), Input('my-toggle-switch', 'value'))
def update_output(value):
    if value == True:
        ret = "ON"
    elif value == False:
        ret = "OFF"
    ValueStorage.write_to_csv_light(ret)
    # return 'The switch is {}.'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)



