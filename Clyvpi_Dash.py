import dash
from dash.dependencies import Input, Output
import dash_daq as daq
from dash import html

app = dash.Dash(__name__)

tempVal = 23
#print("Temp val: ")
#val = input("Enter your value: ")

app.layout = html.Div([
    daq.Gauge(
        id='my-gauge-1',
        label="Temperature",
        color={"gradient": True, "ranges": {"Purple": [-30, -10], "Yellow": [-10, 20], "Red": [20, 40]}},
        showCurrentValue=True,
        units="C",
        size=450,
        value=23,
        max=40,
        min=-30,
    ),
    daq.ToggleSwitch(
        id='my-toggle-switch',
        value=False
    ),
    html.Div(id='my-toggle-switch-output')
])

@app.callback(
    Output('my-toggle-switch-output', 'children'),
    Input('my-toggle-switch', 'value')
)

def update_output(value):
    if value == True:
        ret = "true"
        # Clyvpi_MQTT.client.publish("IoTlab/LEDLight", "ON")
    elif value == False:
        ret = "false"
            # Clyvpi_MQTT.client.publish("IoTlab/LEDLight", "OFF")
    return 'The switch is {}.'.format(value)

@app.callback(Output('my-gauge-1', 'value'), Input('my-gauge-1', 'value'))
def update_output(value):
    return value

if __name__ == '__main__':
    app.run_server(debug=True)

