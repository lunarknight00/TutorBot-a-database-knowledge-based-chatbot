import dialogflow
import apiai
import json
#import request

import dialogflow_v2

APIAI_TOKEN = 'e8062808ba554838b6bddd3466d029df'
#print("try APIAI reply...")
def reply(msg_content, user_id):
    #msg_content = 'Hello'
	ai = apiai.ApiAI(APIAI_TOKEN)
	request = ai.text_request()
	request.lang = 'en'
	request.session_id = user_id
	request.query = msg_content

	response = request.getresponse()
	s = json.loads(response.read().decode('utf-8'))
	
	if s['result']['action'] == 'input.unknown':
		raise Exception('api.ai cannot reply this message')
	if s['status']['code'] == 200:
		print("use APIAI reply")
		print('return code: ' + str(s['result']['fulfillment']['speech']))
                #return s['result']['fulfillment']['speech'] 

reply('Hello', 1)