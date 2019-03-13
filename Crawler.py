# coding=utf-8

# written by Henry Libo Zhuo
# 2019-03-13

import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

class WebCMS:
    def __init__(self,username,password,path):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome(path)

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
        # TO DO brower the forums website 
        
        # helper function to fetch a table in the website
        table = self.getTable(driver)

        
        # TO DO scrapy data from different forums, bfs
        # TO DO data clean
        # TO DO out put data with csv
        return table

    def getTable(self,driver):
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