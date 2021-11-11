import dash
import plotly.graph_objs as go
import dash_daq as daq
import csv
from dash.dependencies import Input, Output
from dash import dcc
from dash import html

app = dash.Dash(__name__)

tempVal = 23
humidVal = 40

def write_to_csv_light(value):
    with open('Light_file.csv', mode='w') as csv_file:
        fieldnames = ['Parameter', 'Value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Parameter': 'Light', 'Value': f'{value}'})


#fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])

colors = {
    'background': 'grey',
    'text': '#7FDBFF'
}

fig = {
    'layout': {
        'title': 'Test'
    },
    'data': [{
        'x': [1, 2, 3],
        'y': [3, 1, 2]
    }]
}

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div([
        dcc.Graph(id='live-update-graph', animate=True, figure=fig),
        html.Div(id='live-update-text'),
        dcc.Interval(
            id='interval-component',
            interval=1 * 1000,  # in milliseconds
            n_intervals=0
        )

    ]),
    dcc.Input(
        id="TempTextBox",
        type="number",
        placeholder="Temp Threshold",
    ),
    daq.Gauge(
        id='my-gauge-1',
        label="Temperature",
        color={"gradient": True, "ranges": {"Blue": [-30, -16], "Yellow": [-16, 20], "Red": [20, 40]}},
        showCurrentValue=True,
        units="C",
        size=200,
        value=tempVal,
        max=40,
        min=-30,
    ),
    daq.Gauge(
        id='my-gauge-2',
        label="Humidity ",
        color={"gradient": True, "ranges": {"Blue": [-30, -16], "Yellow": [-16, 20], "Red": [20, 40]}},
        showCurrentValue=True,
        units="%",
        size=200,
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


@app.callback(Output('live-update-text', 'children'), Input('interval-component', 'n_intervals'))
def update_output(n_intervals):
    return n_intervals

@app.callback(
    Output("TempTextBox", "value"), Input("TempTextBox", "value"))
def update_output(value):
    return value

@app.callback(Output('my-toggle-switch-output', 'children'), Input('my-toggle-switch', 'value'))
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

