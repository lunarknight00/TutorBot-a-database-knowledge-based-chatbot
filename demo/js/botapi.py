from flask import Flask, request
from flask_restplus import Resource, Api
import json
import apiai
from flask_cors import CORS


import requests

# from werkzeug.exceptions import BadRequest
# raise BadRequest()
def match_search(keyword, operator="or",fuzziness="AUTO",msm="50%",top_n=3,link="http://35.189.30.30:9200/qaset/COMP9311/_search"): #msm:minimum_should_match
    """
    settings about msm:
    https://www.elastic.co/guide/en/elasticsearch/reference/5.6/query-dsl-minimum-should-match.html#query-dsl-minimum-should-match
    """
    with open("test1.txt",'w') as f:
        f.write(keyword)
    data_dic = {"query":{"match":{"question":{"query":keyword,"operator":operator,"minimum_should_match":msm,"fuzziness":fuzziness}}}}
    r = requests.get(link, data=json.dumps(data_dic),headers={'Content-Type':'application/json'})

    response = json.loads(r.text)
    total_find = response["hits"]["total"]
    max_score = response["hits"]["max_score"]
    top_doc = response["hits"]["hits"][:top_n]
    res = {}
    for i in range(3):
        res[str(i)]=top_doc[i]
    return total_find, max_score, json.dumps(res)






app = Flask(__name__)
CORS(app)
api = Api(app)

todos = {}
question = ''
anwser = ''

todos = {}


@api.route('/chat/<string:question>')
class TodoSimple(Resource):
    def get(self,question):
        APIAI_TOKEN = 'e8062808ba554838b6bddd3466d029df'

        ai = apiai.ApiAI(APIAI_TOKEN)
        airequest = ai.text_request()
        airequest.lang = 'en'
        airequest.session_id = 1
        airequest.query = question

        response = airequest.getresponse()
        s = json.loads(response.read().decode('utf-8'))
        print(s['result']['action'])
        print(question)
        print(type(question))

        if s['status']['code'] == 200:
            if 'who' in  question or 'Who' in question:
                if 'are' in question:
                    if 'you' in question:
                        return 'I am a tutor robot of Magnum Opus!'

        if s['result']['action'] == 'input.unknown':

            resstr = match_search(question)[2]
            # print(resstr["a"]['_source']['question'])
            #
            # q1 = resstr["a"]['_source']['question']
            # questionset = []
            # answerset = []
            # print(type(resstr))
            # a=json.dumps(resstr)
            # print( a)
            # print(resstr)
            print(match_search(question))
            return resstr.replace("\\n","").replace("\n",""), 200

        if s['status']['code'] == 200:
            anwser = str(s['result']['fulfillment']['speech'])
            return anwser


            #return "Sorry could't understand your question."


            #return {todo_id: todos[todo_id]}

    # def put(self):
    #
    #     APIAI_TOKEN = 'e8062808ba554838b6bddd3466d029df'
    #     todos[todo_id] = request.form['data']
    #     ai = apiai.ApiAI(APIAI_TOKEN)
    #     airequest = ai.text_request()
    #     airequest.lang = 'en'
    #     airequest.session_id = 1
    #     airequest.query = todos[todo_id]
    #
    #     response = airequest.getresponse()
    #     s = json.loads(response.read().decode('utf-8'))
    #
    #     if s['result']['action'] == 'input.unknown':
    #         return "Sorry could't understand your question."
    #     if s['status']['code'] == 200:
    #         # print("use APIAI reply")
    #         # return str(s['result']['fulfillment']['speech'])
    #         question = str(s['result']['fulfillment']['speech'])
    #         return {todo_id: question}
    #
    #
    #         # return {todo_id: todos[todo_id]}


# @api.route('/hello')
# class HelloWorld(Resource):
#     def get(self):
#         return {'hello': 'world'}

@api.route('/es/<string:keyword>')
class es(Resource):
    def get(self,keyword):
        print(keyword)
        print(str(match_search(keyword)))
        return str(match_search(keyword)),200



if __name__ == '__main__':
    app.run(debug=True)