import json
import requests
import apiai
from nltk.corpus import stopwords

keyword_filter = lambda x:' '.join([word for word in x.split() if word not in (stopwords.words('english'))])

def comprehensive_search(keyword,operator="or",\
    fuzziness="AUTO",msm="50%",top_n=3,\
    keyword_filter=None):

    def dialogflow_search(keyword):
        APIAI_TOKEN = 'e8062808ba554838b6bddd3466d029df'
    
        ai = apiai.ApiAI(APIAI_TOKEN)
        airequest = ai.text_request()
        airequest.lang = 'en'
        airequest.session_id = 1
        airequest.query = keyword
        response = airequest.getresponse()
        s = json.loads(response.read().decode('utf-8'))
    
        return s

    def match_search(keyword, operator="or",\
    	fuzziness="AUTO",msm="50%",top_n=3,\
    	link="http://35.189.30.30:9200/qaset/COMP9311/_search",\
    	keyword_filter=None): #msm:minimum_should_match
        """
        settings about msm:
        https://www.elastic.co/guide/en/elasticsearch/reference/5.6/query-dsl-minimum-should-match.html#query-dsl-minimum-should-match
        """
        if keyword_filter:
        	keyword = keyword_filter(keyword)
        data_dic = {"query":{"match":{"question":{"query":keyword,"operator":operator,"minimum_should_match":msm,"fuzziness":fuzziness}}}}
        r = requests.get(link, data=json.dumps(data_dic),headers={'Content-Type':'application/json'})
    
        response = json.loads(r.text)
        total_find = response["hits"]["total"]
        max_score = response["hits"]["max_score"]
        top_doc = response["hits"]["hits"][:top_n]
        
        return total_find, max_score, top_doc


    response = match_search(keyword, operator=operator,\
        fuzziness=fuzziness,msm=msm,top_n=top_n,\
        link="http://35.189.30.30:9200/qaset_slides/COMP9311/_search",\
        keyword_filter=keyword_filter)
    if response[0]:
        return json.dumps(response[2])
    else:
        response = dialogflow_search(keyword)
        if response["result"]["action"] != "input.unknown":
            return response["result"]["fulfillment"]["speech"]
        else:
            response = match_search(keyword, operator=operator,\
                fuzziness=fuzziness,msm=msm,top_n=top_n,\
                link="http://35.189.30.30:9200/qaset/COMP9311/_search",\
                keyword_filter=keyword_filter)
            if response[0]:
                return json.dumps(response[2])
    return "Sorry, I don't understand what you said..."


# print(match_search("what the fuck",msm="50%",keyword_filter=keyword_filter,fuzziness=0))
# print(comprehensive_search("i don't want to study"))
