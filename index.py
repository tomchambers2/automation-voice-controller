import wit
import paho.mqtt.client as mqtt
import os
import json

wit_token = os.environ['WIT_TOKEN']

wit.init()

def set_lights_state(action):
	print 'Send lights message, set to {}'.format(action)
	client.publish('lights/{}'.format(action))

def process_response(response):
	parsedResponse = json.loads(response)
	intent = parsedResponse['outcomes'][0]['intent']
	print intent
	if intent == 'lights':
		action = parsedResponse['outcomes'][0]['entities']['on_off'][0]['value']
		print action
		set_lights_state(action)

	wit.voice_query_auto_async(wit_token, process_response)

def on_connect(client, userdata, rc):
	print('Connected with result code '+str(rc))
	client.subscribe('lights/#')	

client = mqtt.Client("voice_controller")
client.on_connect = on_connect
client.connect('localhost', 1883, 60)

wit.voice_query_auto_async(wit_token, process_response)

client.loop_forever()