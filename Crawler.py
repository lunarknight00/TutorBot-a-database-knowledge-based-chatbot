# coding=utf-8

# written by Henry Libo Zhuo
# class design version
# 2019-03-20

from bs4 import BeautifulSoup
from selenium import webdriver
import requests
import pandas as pd
import re,time,csv

class WebCMS:
    base = "https://webcms3.cse.unsw.edu.au"
    def __init__(self,username,password,path,tag = "forum",courseCode,semster,year):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(path)
        self.tag = self.genTags()
        self.year = year
        self.semster = semster
        self.courseCode = courseCode
        self.vips = self.extractVIP()
        self.tags = self.
        self.questions, self.replies = self.crawl()
        self.Index = self.Index()
        self.SecondIndex = self.SecondIndex()

    def courseURL(self):
        return "https://webcms3.cse.unsw.edu.au/" + self.courseCode + '/' + self.year + 's'+ self.year +"/"

    def genTags(self):
        return len(self.questions)

    def login(self):
        driver = self.driver
        driver.get("https://webcms3.cse.unsw.edu.au/login")
        for usname in self.username:
            driver.find_element_by_name("zid").send_keys(usname)
            time.sleep(0.2)
        for pwd in self.password:
            driver.find_element_by_name("password").send_keys(pwd)
            time.sleep(0.2)
        time.sleep(10)
        driver.find_element_by_xpath("//*[@id='webcms3top']/div/div[1]/div/div[2]/div/div/form/button").click()
        return self.crawl()
    
    def Index(self):
        driver = self.driver
        driver.get(self.courseURL(self) +"forums/")
        page = driver.page_source
        soup = BeautifulSoup(page,"html.parser")
        table = soup.find_all("tr")
        forum = []
        for row in table:
            cols = row.find_all("td")
            for col in cols:
                try:
                    nb = int(col.get_text())
                    if nb > 0:
                        tmp = row.find("a").get("href")
                        if  re.findall("forums",tmp) and len(tmp) > 22:
                            forum.append(base + tmp)
                except:
                    continue
        return forum

    def SecondIndex(self):
        driver = self.driver
        visited,forum1 = set(),list()
        for url in self.Index:
            driver.get(url)
            page = driver.page_source
            soup = BeautifulSoup(page,"html.parser")
            links = soup.find_all("a")
            for link in links:
                tmp = link.get("href")
                if tmp in visited:
                    continue
                visited.add(tmp)
                if  re.findall("forums",tmp) and len(tmp) > 22:
                    forum1.append(base + tmp)
        return forum1

    def crawl(self.):
        driver = self.driver
        questions,replies = list(),list()
        for url in forum1:
            driver.get(url)
            time.sleep(5)
            page = driver.page_source
            soup = BeautifulSoup(page,"html.parser")
            reply, question = str(),str()
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
        return questions,replies

    def output(self,filename):
        self.tags = [self.tag for _ in range(len(questions))]
        with open(filename, 'w', newline='',encoding='utf-8') as csvfile:
            fieldnames = ["Source", "Question", "reply"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for s, q, r in zip(self.tags, self.questions, self.replies):
                writer.writerow({"Source":s,"Question": q, "reply":r})

    def extractVIP(self):
        driver = self.driver
        html = driver.page_source
        soup = BeautifulSoup(html,"lxml")
        vips = []
        for p in soup.find_all("li",{"class":"list-group-item"}):
            if p.find("span",{"class":"label label-primary"}):
                vip = p.find("a").get_text()
                vips.append(vip)
        return vips

    def getTable(self):
        driver = self.driver
        html = driver.page_source
        soup = BeautifulSoup(html,"lxml")
        table = soup.find_all("table")
        n_columns = 0
        n_rows=0
        column_names = []
        # Find number of rows and columns
        # we also find the column titles if we can
        for row in table.find_all('tr'):
            # Determine the number of rows in the table
            td_tags = row.find_all('td')
            if len(td_tags) > 0:
                n_rows+=1
                if n_columns == 0:
                    # Set the number of columns for our table
                    n_columns = len(td_tags)
            # Handle column names if we find them
            th_tags = row.find_all('th') 
            if len(th_tags) > 0 and len(column_names) == 0:
                for th in th_tags:
                    column_names.append(th.get_text())
        # Safeguard on Column Titles
        if len(column_names) > 0 and len(column_names) != n_columns:
            raise Exception("Column titles do not match the number of columns")
        columns = column_names if len(column_names) > 0 else range(0,n_columns)
        df = pd.DataFrame(columns = columns,index= range(0,n_rows))
        row_marker = 0
        for row in table.find_all('tr'):
            column_marker = 0
            columns = row.find_all('td')
            for column in columns:
                df.iat[row_marker,column_marker] = column.get_text()
                column_marker += 1
            if len(columns) > 0:
                row_marker += 1
        # Convert to float if possible
        for col in df:
            try:
                df[col] = df[col].astype(float)
            except ValueError:
                pass
        return df
