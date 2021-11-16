import dash
import plotly.graph_objs as go
import dash_daq as daq
import csv
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import time

app = dash.Dash(__name__)

def write_to_csv_light(value):
    with open('Light_file.csv', mode='w') as csv_file:
        fieldnames = ['Parameter', 'Value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Parameter': 'Light', 'Value': f'{value}'})

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

tempGaugeUpdate = go.Figure(go.Indicator(
    mode="gauge+number",
    value=50,
    number={'suffix': " C°"},
    title={'text': 'Temperature:'},
    # domain={'x': [0.15, 0.8], 'y': [0.2, 0.9]},
    gauge={
        'axis': {'range': [-60, 60]},
        # 'shape': "bullet",
        'steps': [
            {'range': [-60, 0], 'color': "blue"},
            {'range': [0, 40], 'color': "yellow"},
            {'range': [40, 60], 'color': "red"}
        ],
        'threshold': {'line': {'color': "black", 'width': 10}, 'thickness': 0.75, 'value': 50}
    }
))

humGaugeUpdate = go.Figure(go.Indicator(
    mode="gauge+number",
    value=60,
    number={'suffix': " %"},
    title={'text': 'Humidity:'},
    # domain={'x': [0.1, 1], 'y': [0.2, 0.9]},
    gauge={
        'axis': {'range': [0, 100]},
        # 'shape': "bullet",
        'steps': [
            {'range': [0, 33], 'color': "blue"},
            {'range': [33, 66], 'color': "yellow"},
            {'range': [66, 100], 'color': "red"}
        ],
        'threshold': {'line': {'color': "black", 'width': 10}, 'thickness': 0.75, 'value': 60}
    }
))

lightGaugeUpdate = go.Figure(go.Indicator(
    mode="gauge+number",
    value=60,
    number={'suffix': " %"},
    title={'text': 'Light Intensity:'},
    # domain={'x': [0.1, 1], 'y': [0.2, 0.9]},
    gauge={
        'axis': {'range': [0, 100]},
        # 'shape': "bullet",
        'steps': [
            {'range': [0, 33], 'color': "#80A413"},
            {'range': [33, 66], 'color': "#C8FF00"},
            {'range': [66, 100], 'color': "#FFE800"}
        ],
        'threshold': {'line': {'color': "black", 'width': 10}, 'thickness': 0.75, 'value': 60}
    }
))

app.layout = html.Div(style={'text-align': 'center'}, children=[
    html.H1('Clyvpi Dashboard', style={'textAlign': 'center'}),
    html.Br(),
    html.H2('WELCOME: xxx'),
    html.H3('RFID#: xxx'),
    html.Br(),
    html.Br(),
    dcc.Graph(id='tempGaugeUpdate', figure=tempGaugeUpdate, style={'display': 'inline-block', 'width': '48%'}),
    dcc.Graph(id='humGaugeUpdate', figure=humGaugeUpdate, style={'display': 'inline-block', 'width': '48%'}),
    dcc.Graph(id='lightGaugeUpdate', figure=lightGaugeUpdate, style={'display': 'inline-block', 'width': '48%'}),
    dcc.Interval(id='intervalComponent', interval=1 * 3000, n_intervals=0),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H3('Temperature Threshold'),
    dcc.Input(
        id="TempTextBox",
        type="number",
        placeholder="Temp Sensor Threshold",
        style={'width': '15%'}
    ),
    html.H3('Light Threshold'),
    dcc.Input(
        id="LightSensorTextBox",
        type="number",
        placeholder="Light Sensor Threshold",
        style={'width': '15%'}
    ),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    html.H2('Turn LED ON/OFF'),
    daq.ToggleSwitch(
        id='my-toggle-switch',
        value=False
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
    tempValMQTT = float(read_csv_MQTT_Temperature())
    humValMQTT = float(read_csv_MQTT_Humidity())
    lightMQTT = float(read_csv_MQTT_Light())
    tempGaugeUpdate = go.Figure(go.Indicator(
        mode="gauge+number",
        value=tempValMQTT,
        number={'suffix': " C°"},
        title={'text': 'Temperature:'},
        gauge={
            'axis': {'range': [-60, 60]},
            'steps': [
                {'range': [-60, 0], 'color': "blue"},
                {'range': [0, 40], 'color': "yellow"},
                {'range': [40, 60], 'color': "red"}
            ],
            'threshold': {'line': {'color': "black", 'width': 10}, 'thickness': 0.75, 'value': tempValMQTT}
        }
    ))
    humGaugeUpdate = go.Figure(go.Indicator(
        mode="gauge+number",
        value=humValMQTT,
        number={'suffix': " %"},
        title={'text': 'Humidity:'},
        gauge={
            'axis': {'range': [0, 100]},
            'steps': [
                {'range': [0, 33], 'color': "#b0ebff"},
                {'range': [33, 66], 'color': "#57d5ff"},
                {'range': [66, 100], 'color': "#00b2ee"}
            ],
            'threshold': {'line': {'color': "black", 'width': 10}, 'thickness': 0.75, 'value': humValMQTT}
        }
    ))
    lightGaugeUpdate = go.Figure(go.Indicator(
        mode="gauge+number",
        value=lightMQTT,
        number={'suffix': " %"},
        title={'text': 'Light Intensity:'},
        gauge={
            'axis': {'range': [0, 100]},
            'steps': [
                {'range': [0, 33], 'color': "#80A413"},
                {'range': [33, 66], 'color': "#C8FF00"},
                {'range': [66, 100], 'color': "#FFE800"}
            ],
            'threshold': {'line': {'color': "black", 'width': 10}, 'thickness': 0.75, 'value': lightMQTT}
        }
    ))
    return [tempGaugeUpdate, humGaugeUpdate, lightGaugeUpdate]

@app.callback(
    Output("TempTextBox", "value"), Input("TempTextBox", "value"))
def update_output(value):
    return value

@app.callback(
    Output("LightSensorTextBox", "value"), Input("LightSensorTextBox", "value"))
def update_output(value):
    time.sleep(3)
    write_to_csv_light_threshold(value)

@app.callback(Output('my-toggle-switch-output', 'children'), Input('my-toggle-switch', 'value'))
def update_output(value):
    if value == True:
        ret = "true"
        write_to_csv_light("ON")
    elif value == False:
        ret = "false"
        write_to_csv_light("OFF")
    return 'The switch is {}.'.format(value)

if __name__ == '__main__':
    app.run_server(debug=True)

