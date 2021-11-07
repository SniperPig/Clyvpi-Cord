import dash
from dash.dependencies import Input, Output
import dash_daq as daq
from dash import html
import csv

app = dash.Dash(__name__)

tempVal = 23
humidVal = 40

#print("Temp val: ")
#val = input("Enter your value: ")

def write_to_csv_light(value):
    with open('Light_file.csv', mode='w') as csv_file:
        fieldnames = ['Parameter', 'Value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Parameter': 'Light', 'Value': f'{value}'})

app.layout = html.Div([
    daq.Gauge(
        id='my-gauge-1',
        label="Temperature",
        color={"gradient": True, "ranges": {"Blue": [-30, -16], "Yellow": [-16, 20], "Red": [20, 40]}},
        showCurrentValue=True,
        units="C",
        size=450,
        value=tempVal,
        max=40,
        min=-30,
    ),
    daq.Gauge(
        id='my-gauge-2',
        label="Humidity ",
        color={"gradient": True, "ranges": {"Blue": [-30, -16], "Yellow": [-16, 20], "Red": [20, 40]}},
        showCurrentValue=True,
        units="C",
        size=450,
        value=humidVal,
        max=100,
        min=0,
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
        write_to_csv_light("ON")
    elif value == False:
        ret = "false"
        write_to_csv_light("OFF")
    return 'The switch is {}.'.format(value)

@app.callback(Output('my-gauge-1', 'value'), Input('my-gauge-1', 'value'))
def update_output(value):
    return value

@app.callback(Output('my-gauge-2', 'value'), Input('my-gauge-2', 'value'))
def update_output(value):
    return value

if __name__ == '__main__':
    app.run_server(debug=True)

