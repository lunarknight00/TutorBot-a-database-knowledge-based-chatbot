#  noted
#  add your zid and password first to run the program
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
import re,time,csv

# extract all tutor and lecturer list
def extractVIP(soup):
    vips = []
    for p in soup.find_all("li",{"class":"list-group-item"}):
        if p.find("span",{"class":"label label-primary"}):
            vip = p.find("a").get_text()
            vips.append(vip)
 


vips = []
tag = []
questions = []
replies =[]


browser = webdriver.Chrome(executable_path=r"C:\Users\zhuol\Desktop\COMP9900\crawler\chromedriver.exe")
browser.get("https://webcms3.cse.unsw.edu.au/login")
zid = browser.find_element_by_name("zid")
pw = browser.find_element_by_name("password")


#  noted
#  add your zid and password here
zid.send_keys("")
pw.send_keys("")

button = browser.find_element_by_xpath("//*[@id='webcms3top']/div/div[1]/div/div[2]/div/div/form/button")
button.click()

base = "https://webcms3.cse.unsw.edu.au/"

forum0 = []

def load_index_forum(url,browser):
	browser.get(url)
	time.sleep(3)
	page = browser.page_source
	soup = BeautifulSoup(page,"html.parser")
	for p in soup.find_all("li",{"class":"list-group-item"}):
            if p.find("span",{"class":"label label-primary"}):
                vip = p.find("a").get_text()
                vips.append(vip)
	table = soup.find_all("tr")
	for row in table:
	    cols = row.find_all("td")
	    for col in cols:
	        try:
	            nb = int(col.get_text())
	            if nb > 0:
	                tmp = row.find("a").get("href")
	                if  re.findall("forums",tmp) and len(tmp) > 22:
	                    forum0.append(base + tmp)
	        except:
	            continue
marker0 = 0
for courseCode in ['COMP9311','COMP3311']:
	for year in range(15,19):
		for i in range(1,3):	            
			try:
                            load_index_forum(base + courseCode + '/' + str(year) + 's'+ str(i) +"/"+"forums/",browser)
			    #text = browser.find_element_by_xpath('//*[@id="webcms3top"]/div[1]/div[1]/div/div/h2').text
			    #continue
			except:
                            continue
                        
			    #load_index_forum(base + courseCode + '/' + year + 's'+ i +"/"+"forums/",browser)

forum1 = []
for url in forum0:
    browser.get(url)
    time.sleep(5)
    page = browser.page_source
    soup = BeautifulSoup(page,"html.parser")
    table = soup.find_all("tr")
    for row in table:
        cols = row.find_all("td")
        for col in cols:
            try:
                nb = int(col.get_text())
                if nb > 0:
                    tmp = row.find("a").get("href")
                    print(tmp)
                    forum1.append(base + tmp)
            except:
                continue

for url in forum1:
    browser.get(url)
    time.sleep(5)
    page = browser.page_source
    soup = BeautifulSoup(page,"html.parser")
    reply,question = str(),str()
    aset = soup.find_all("div",{"class":"comment-content"})
    for tmp in aset:
        person = tmp.find("header").find("a").get_text()
        text = tmp.get_text()
        lines = [line.strip() for line in text.splitlines()]
        comment = [line for line in lines[1:len(lines)-1] if len(line)>0]
        try:
            img = tmp.find("img").get("src")
            comment.append(base + img)
        except:
            pass
        if person in vips:
            reply += " " + " ".join(comment)
        else:
            question += " " + " ".join(comment)
    if len(reply) > 0:
        if question not in set(questions) and reply not in set(replies):
            questions.append(question)
            replies.append(reply)

tag = ["forum" for _ in range(len(questions))]

tag = ["forum" for _ in range(len(questions))]
with open('forumdata.csv', 'w', newline='',encoding='utf-8') as csvfile:
    fieldnames = ["Source", "Question", "reply"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for s, q, r in zip(tag, questions, replies):
        writer.writerow({"Source":s,"Question": q, "reply":r})
