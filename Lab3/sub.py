# https://github.com/pholur/180D_sample
import random
from paho.mqtt import client as mqtt_client


broker = 'broker.emqx.io'
port = 1883
topic = "/python/mqtt"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'


def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()

# import paho.mqtt.client as mqtt
#
# #0. define callbacks - functions that run when events happen.
# # The callback for when the client receives a CONNACK response from the server
# def on_connect(client, userdata, flags, rc):
# 	print("Connection returned result: " + str(rc))
#
# 	# Subscribing in on_connect() means that if we lose the connection and
# 	# reconnect then subscriptoins will be renewed
# 	client.subscribe("ece180d/text", qos=1)
#
# # The callback of the client when it disconnects.
# def on_disconnect(client, userdata, rc):
# 	if rc != 0:
# 		print('Unexcpected Disconnect')
# 	else:
# 		print('Expected Disconnect')
# # The default message callback
# # (you can create separate calllbacks per subscribed topic)
# def on_message(client, userdata, message):
# 	print('Received message: "' + str(message.payload) + '" on topic "' +
# 			message.topic + '" with QoS ' + str(message.qos))
#
# # 1. create a client instance.
# client = mqtt.Client()
# # add additional client options (security, certifications, etc.)
# # many default options should be good to start off
# # add callbacks to Client
# client.on_connect = on_connect
# client.on_disconnect = on_disconnect
# client.on_message = on_message
#
# # 2. connect to a broker using one of the connect*() functions
# client.connect_async('mqtt.eclipse.org')
# # client.connect("mqtt.eclipse.org")
#
# # 3. call one of the loop*() functions to maintain network traffic flow with the broker.
# client.loop_start()
# # client.loop_forever()
#
# while True:
# 	pass
# # use subscribe() to subscribe to a topic and receive messages
#
# #use publish() to publish messages to the broker
#
# #use disconnect() to disconnect from the broker
# client.loop_stop()
# client.disconnect()
