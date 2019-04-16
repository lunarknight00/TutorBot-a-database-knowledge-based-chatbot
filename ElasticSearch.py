import json
import requests
from nltk.corpus import stopwords

keyword_filter = lambda x:' '.join([word for word in x.split() if word not in (stopwords.words('english'))])

def match_search(keyword, operator="or",msm="50%",top_n=3,
                 link="http://35.231.149.211:9200/qaset/COMP9311/_search",
                keyword_filter=None): #msm:minimum_should_match
    """
    settings about msm:
    https://www.elastic.co/guide/en/elasticsearch/reference/5.6/query-dsl-minimum-should-match.html#query-dsl-minimum-should-match
    """
    if keyword_filter:
        keyword = keyword_filter(keyword)
    
    data_dic = {"query":{"match":{"question":{"query":keyword,"operator":operator,"minimum_should_match":msm}}}}
    r = requests.get(link, data=json.dumps(data_dic),headers={'Content-Type':'application/json'})

    response = json.loads(r.text)
    total_find = response["hits"]["total"]
    max_score = response["hits"]["max_score"]
    top_doc = response["hits"]["hits"][:top_n]
    return total_find,max_score,top_doc


print(match_search("what the fuck",msm="50%"))