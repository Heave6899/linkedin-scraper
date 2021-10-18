import time
from typing import Dict
from requests.models import cookiejar_from_dict
from selenium import webdriver
import requests
from bs4 import BeautifulSoup as bs
from random import choice
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
import json
from pymongo import MongoClient
from pprint import pprint
import csv
from selenium.webdriver.firefox.options import Options
import sys
import urllib

def connect_to_db():
    client = MongoClient(
        "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")
    db = client.cloudeagle
    return db


# Issue the serverStatus command and print the results

def request_opener():
    try:
        opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({'http': 'http://lum-customer-c_3b483b89-zone-residentialrotator:maau0b8jhjrq@zproxy.lum-superproxy.io:22225',
        'https': 'http://lum-customer-c_3b483b89-zone-residentialrotator:maau0b8jhjrq@zproxy.lum-superproxy.io:22225'}))

        # print(opener.open('http://lumtest.com/myip.json').read())
        opener.open('https://www.linkedin.com')
        time.sleep(10)
        x = opener.open('https://www.google.com')
        return opener
    except Exception as e:
        raise e


def scrape_linkedin(link, opener):
    try:
        print("inside scrape")
        response = opener.open(link)
        time.sleep(15)
        print(response.read())
        response = opener.open(link.rstrip('/', 1)[0] + '/about')
        time.sleep(15)
        source = response.read()
        print('source:',source)
        # chrome.get(link)
       
        if 'auth' in response.current_url:
            print('Auth Wall Detected')
            exit()
        # chrome.get(chrome.current_url + 'about')
        # start = time.time()
        # lastHeight = chrome.execute_script("return document.body.scrollHeight")
        # while True:
            # chrome.execute_script(
            #     "window.scrollTo(0, document.body.scrollHeight);")
            # time.sleep(5)
            # newHeight = chrome.execute_script(
            #     "return document.body.scrollHeight")
            # if newHeight == lastHeight:
            #     break
            # lastHeight = newHeight
            # end = time.time()
            # if round(end-start) > 20:
            #     break

        # company_page = chrome.page_source

        linkedin_soup = bs(source.encode("utf-8"), 'html.parser')
        for script in linkedin_soup(["script", "style"]):
            script.extract()    # rip it out

        text = linkedin_soup.get_text()

        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip()
                  for line in lines for phrase in line.split("  "))
        text = [chunk for chunk in chunks if chunk]
        jsonOutput = {}
        for i in range(len(text)):
            if text[i] == 'Industry':
                jsonOutput['Industry'] = text[i+1]
            if text[i] == 'Company size':
                jsonOutput['Company Size'] = text[i+1]
            if text[i] == 'Website':
                jsonOutput['Website'] = text[i+1]
        print('function', jsonOutput)
        return jsonOutput

    except Exception as e:
        # chrome.quit()
        raise Exception


def save_csv(jsonOutput, csv_columns):
    csv_file = "StackData.csv"
    with open(csv_file, 'a') as f:
        w = csv.DictWriter(f, csv_columns)
        w.writerow(jsonOutput)


if __name__ == "__main__":
    links = []
    path = '../WebScrap'
    csv_columns = ['Company Name', 'Software',
                   'Current Funding Level', 'Company Size', 'Website', 'Industry']
    user_agent = 'Mozilla/5.0 CK={} (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'
    USERNAME = "krdrxebzvrvdnntgst@sdvgeft.com"
    PASSWORD = "123Vansh"

    non_linked_in_companies = []
    db = connect_to_db()
    activeCompanies = db.activeCompanies
    stackData = db.stackData
    for document in activeCompanies.find().skip(int(sys.argv[1])).limit(int(sys.argv[2])):
        if document.get('linkedin') is not None:
            links.append(
                (document.get('uuid'), document.get('linkedin')['value']))
        else:
            non_linked_in_companies.append(document.get('uuid'))
        # print(len(links))
        if len(links) == 1:
            # print(links)
            # while True:
            #     try:
                    
            #         break
            #     except Exception as e:
            #         print(e)
            for i in links:
                try:
                    print(i)
                    document = activeCompanies.find_one({'uuid': i[0]})
                    if document:
                        jsonOutput = None
                        while jsonOutput is None:
                          try:
                              opener = request_opener()
                              jsonOutput = scrape_linkedin(i[1], opener)
                              print('jsonOutput',jsonOutput)
                          except Exception as e:
                              print(e)
                        
                        print('scrapped:', jsonOutput, type(jsonOutput))
                        if isinstance(jsonOutput, Dict):
                            # jsonOutput['uuid'] = i[0]
                            jsonOutput['Company Name'] = document.get('identifier')[
                                'value']
                            stack = []
                            for stacks in stackData.find({'org_uuid': i[0]}):
                                stack.append(stacks.get(
                                    'product_identifier')['value'])
                            if len(stack) == 0:
                                jsonOutput['Software'] = ''
                            else:
                                jsonOutput['Software'] = '~'.join(stack)
                            if 'Company Size' not in jsonOutput:
                                jsonOutput['Company Size'] = ''
                            if 'Website' not in jsonOutput:
                                if document.get('website') is not None:
                                    jsonOutput['Website'] = document.get('website')[
                                        'value']
                                else:
                                    jsonOutput['Website'] = ''
                            if document.get('equity_funding_total') is not None:
                                jsonOutput['Current Funding Level'] = document.get(
                                    'equity_funding_total')['value_usd']
                            elif document.get('funding_total') is not None:
                                jsonOutput['Current Funding Level'] = document.get('funding_total')[
                                    'value_usd']
                            else:
                                jsonOutput['Current Funding Level'] = ''
                            if 'Industry' not in jsonOutput:
                                if document.get('categories') is not None:
                                    category = []
                                    industries = document.get('categories')
                                    for i in industries:
                                        category.append(i['value'])
                                    jsonOutput['Industry'] = '~'.join(category)
                                else:
                                    jsonOutput['Industry'] = ''
                            save_csv(jsonOutput, csv_columns)
                    else:
                        jsonOutput = {}
                        # jsonOutput['uuid'] = i[0]
                        stack = []
                        for stacks in stackData.find({'org_uuid': i[0]}):
                            stack.append(stacks.get(
                                'product_identifier')['value'])
                        if len(stack) == 0:
                            jsonOutput['Software'] = ''
                        else:
                            jsonOutput['Software'] = '~'.join(stack)
                        jsonOutput['Company Name'] = document.get('identifier')[
                            'value']
                        if document.get('equity_funding_total') is not None:
                            jsonOutput['Current Funding Level'] = document.get(
                                'equity_funding_total')['value_usd']
                        elif document.get('funding_total') is not None:
                            jsonOutput['Current Funding Level'] = document.get('funding_total')[
                                'value_usd']
                        else:
                            jsonOutput['Current Funding Level'] = ''
                        if document.get('num_employees_enum') is not None:
                            try:
                                size = document.get('num_employees_enum').split('_')
                                jsonOutput['Company Size'] = str(
                                int(size[1])) + "-" + str(int(size[2])) + " employees"
                            except:
                                jsonOutput['Company Size'] = 'Max employees'
                        else:
                            jsonOutput['Company Size'] = ''
                        if document.get('website') is not None:
                            jsonOutput['Website'] = document.get('website')[
                                'value']
                        else:
                            jsonOutput['Website'] = ''
                        if document.get('categories') is not None:
                            category = []
                            industries = document.get('categories')
                            for i in industries:
                                category.append(i['value'])
                            jsonOutput['Industry'] = '~'.join(category)
                        else:
                            jsonOutput['Industry'] = ''
                        save_csv(jsonOutput, csv_columns)
                except Exception as e:
                    print(e)
            # chrome.quit()
            links = []
        else:
            if len(non_linked_in_companies) > 0:
                # print(non_linked_in_companies[0])
                for i in non_linked_in_companies:
                    jsonOutput = {}
                    # jsonOutput['uuid'] = i[0]
                    stack = []
                    for stacks in stackData.find({'org_uuid': i[0]}):
                        stack.append(stacks.get('product_identifier')['value'])
                    if len(stack) == 0:
                        jsonOutput['Software'] = ''
                    else:
                        jsonOutput['Software'] = '~'.join(stack)
                    jsonOutput['Company Name'] = document.get('identifier')[
                        'value']
                    if document.get('equity_funding_total') is not None:
                        jsonOutput['Current Funding Level'] = document.get(
                            'equity_funding_total')['value_usd']
                    elif document.get('funding_total') is not None:
                        jsonOutput['Current Funding Level'] = document.get('funding_total')[
                            'value_usd']
                    else:
                        jsonOutput['Current Funding Level'] = ''
                    if document.get('num_employees_enum') is not None:
                        try:
                            size = document.get('num_employees_enum').split('_')
                            jsonOutput['Company Size'] = str(
                            int(size[1])) + "-" + str(int(size[2])) + " employees"
                        except:
                            jsonOutput['Company Size'] = 'Max employees'
                    else:
                        jsonOutput['Company Size'] = ''
                    if document.get('website') is not None:
                        jsonOutput['Website'] = document.get('website')[
                            'value']
                    else:
                        jsonOutput['Website'] = ''
                    if document.get('categories') is not None:
                        category = []
                        industries = document.get('categories')
                        for i in industries:
                            category.append(i['value'])
                        jsonOutput['Industry'] = '~'.join(category)
                    else:
                        jsonOutput['Industry'] = ''
                    save_csv(jsonOutput, csv_columns)
                non_linked_in_companies = []
