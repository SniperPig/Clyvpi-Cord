import paho.mqtt.client as mqtt
import dash
from dash.dependencies import Input, Output
import dash_daq as daq
import dash_core_components as dcc
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div([
    daq.Gauge(
        id='my-gauge-1',
        label="Temperature",
        color={"gradient": True, "ranges": {"Blue": [-30, -10], "Yellow": [-10, 20], "Red": [20, 40]}},
        showCurrentValue=True,
        units="C",
        size=450,
        value=2,
        max=40,
        min=-30,
    ),
    dcc.Slider(
        id='my-gauge-slider-1',
        min=-30,
        max=40,
        step=1,
        value=5
    ),
])

@app.callback(Output('my-gauge-1', 'value'), Input('my-gauge-slider-1', 'value'))
def update_output(value):
    return value



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Conndected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("IoTlab/temperature")
    client.subscribe("IoTlab/humidity")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("192.168.1.100", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
if __name__ == '__main__':
    app.run_server(debug=True)
    client.loop_forever()

