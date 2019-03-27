import dialogflow
import apiai
import json
import speech_recognition as sr 
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
		print("Sorry could't understand your question.")
	if s['status']['code'] == 200:
		print("use APIAI reply")
		print(str(s['result']['fulfillment']['speech']))
		#raise Exception('api.ai cannot reply this message')
                #return s['result']['fulfillment']['speech'] 

def voice_iden():
	r = sr.Recognizer()               
	with sr.Microphone() as source: 
		print("Speak Anything :")
		audio = r.listen(source)    
		try:
			text = r.recognize_google(audio)    
			print("You said : {}".format(text))
		except:
			print("Sorry could not recognize your voice")
	return text
	'''
	while(text != 'quiet'):
		reply(text, 1)
		r = sr.Recognizer()                 
		with sr.Microphone() as source:     
			print("Speak Anything :")
			audio = r.listen(source)        
			try:
				text = r.recognize_google(audio)    
				print("You said : {}".format(text))
			except:
				print("Sorry could not recognize your voice") 
		#reply(text, 1).
	print("See you")
	'''

question = input("Enter your question: ")
while(question != 'quit'):
	if question == 'voice' :
		question = voice_iden()
	reply(question, 1)
	question = input("Enter your question ")