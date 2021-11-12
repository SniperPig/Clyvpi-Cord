import dash
import plotly.graph_objs as go
import dash_daq as daq
import csv
from dash.dependencies import Input, Output
from dash import dcc
from dash import html

app = dash.Dash(__name__)

def write_to_csv_light(value):
    with open('Light_file.csv', mode='w') as csv_file:
        fieldnames = ['Parameter', 'Value']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        writer.writerow({'Parameter': 'Light', 'Value': f'{value}'})


colors = {
    'background': 'grey',
    'text': '#7FDBFF'
}

tempGaugeUpdate = go.Figure(go.Indicator(
    mode="gauge+number",
    value=23,
    title={'text': 'Temperature'},
    gauge={
        'axis': {'range': [-60, 60]},
        'shape': "bullet",
        'steps': [
            {'range': [-60, 0], 'color': "blue"},
            {'range': [0, 40], 'color': "yellow"},
            {'range': [40, 60], 'color': "red"}
        ],
        'threshold': {'line': {'color': "black", 'width': 10}, 'thickness': 0.75, 'value': 23}
    }
))

humGaugeUpdate = go.Figure(go.Indicator(
    mode="gauge+number",
    value=60,
    title={'text': 'Humidity'},
    gauge={
        'axis': {'range': [0, 100]},
        'shape': "bullet",
        'steps': [
            {'range': [0, 33], 'color': "blue"},
            {'range': [33, 66], 'color': "yellow"},
            {'range': [66, 100], 'color': "red"}
        ],
        'threshold': {'line': {'color': "black", 'width': 10}, 'thickness': 0.75, 'value': 60}
    }
))

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.Div(id='led_output'),
    dcc.Graph(id='tempGaugeUpdate', figure=tempGaugeUpdate, style={'width': '150vh', 'height': '30vh'}),
    dcc.Graph(id='humGaugeUpdate', figure=humGaugeUpdate, style={'width': '150vh', 'height': '30vh'}),
    dcc.Interval(id='intervalComponent', interval=1 * 3000, n_intervals=0),
    dcc.Input(
        id="TempTextBox",
        type="number",
        placeholder="Temp Threshold",
    ),
    daq.ToggleSwitch(
        id='my-toggle-switch',
        value=False
    ),
    html.Div(id='my-toggle-switch-output')
])

@app.callback([
    Output('tempGaugeUpdate', 'figure'), Output('humGaugeUpdate', 'figure')], [Input('intervalComponent', 'n_intervals')]
)
def update_temp_gauge(n_intervals):
    tempGaugeUpdate = go.Figure(go.Indicator(
        mode="gauge+number",
        value=23,
        title={'text': 'Temperature'},
        gauge={
            'axis': {'range': [-60, 60]},
            'shape': "bullet",
            'steps': [
                {'range': [-60, 0], 'color': "blue"},
                {'range': [0, 40], 'color': "yellow"},
                {'range': [40, 60], 'color': "red"}
            ],
            'threshold': {'line': {'color': "black", 'width': 10}, 'thickness': 0.75, 'value': 23}
        }

    ))
    humGaugeUpdate = go.Figure(go.Indicator(
        mode="gauge+number",
        value=60,
        title={'text': 'Humidity'},
        gauge={
            'axis': {'range': [0, 100]},
            'shape': "bullet",
            'steps': [
                {'range': [0, 33], 'color': "blue"},
                {'range': [33, 66], 'color': "yellow"},
                {'range': [66, 100], 'color': "red"}
            ],
            'threshold': {'line': {'color': "black", 'width': 10}, 'thickness': 0.75, 'value': 60}
        }
    ))
    return [tempGaugeUpdate, humGaugeUpdate]

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

if __name__ == '__main__':
    app.run_server(debug=True)

