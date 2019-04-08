from flask import Flask, request
from flask_restplus import Resource, Api
import json
import apiai
#from werkzeug.exceptions import BadRequest
#raise BadRequest()

app = Flask(__name__)
api = Api(app)

todos = {}
question = ''
anwser = ''

todos = {}
 
@api.route('/<string:todo_id>')
class TodoSimple(Resource):
	def get(self, todo_id):
		return {todo_id: todos[todo_id]}
 
	def put(self, todo_id):

		APIAI_TOKEN = 'e8062808ba554838b6bddd3466d029df'
		todos[todo_id] = request.form['data']
		ai = apiai.ApiAI(APIAI_TOKEN)
		airequest = ai.text_request()
		airequest.lang = 'en'
		airequest.session_id = 1
		airequest.query = todos[todo_id]

		response = airequest.getresponse()
		s = json.loads(response.read().decode('utf-8'))
	
		if s['result']['action'] == 'input.unknown':
			return "Sorry could't understand your question."
		if s['status']['code'] == 200:
		    #print("use APIAI reply")
		    #return str(s['result']['fulfillment']['speech'])
			question = str(s['result']['fulfillment']['speech'])
			return {todo_id: question}


        #return {todo_id: todos[todo_id]}

@api.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}



if __name__ == '__main__':
    app.run(debug=True)


    