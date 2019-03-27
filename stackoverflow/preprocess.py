import csv,html2text
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

def wordsFilter(data):
	stopWords = set(stopwords.words('english'))
	words = word_tokenize(data)
	wordsFiltered = []
	for w in words:
	    if w not in stopWords:
	        wordsFiltered.append(w)
	return " ".join(wordsFiltered)
 
filename = 'QueryResults.csv'

with open('processed.csv', 'w',encoding='utf-8', newline='') as file:
    fieldnames = ["Source", "Question", "Reply"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    writer.writeheader()
    with open(filename, 'r', encoding='utf-8') as csvfile:
    	reader = csv.DictReader(csvfile)
    	for row in reader:
    		q = wordsFilter(html2text.html2text(row["Questions"]))
    		r = wordsFilter(html2text.html2text(row['Answers']))
    		writer.writerow({"Source":'Stackoverflow',"Question":q, "Reply":r})
