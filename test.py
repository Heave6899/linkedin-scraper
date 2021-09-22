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


def connect_to_db():
    client = MongoClient(
        "mongodb://localhost:27017/?readPreference=primary&appname=MongoDB%20Compass&ssl=false")
    db = client.cloudeagle
    return db


# Issue the serverStatus command and print the results

def proxy_generator():
    response = requests.get("https://sslproxies.org/")
    soup = bs(response.content, 'html5lib')
    proxy = {'https': choice(list(map(lambda x: x[0]+':'+x[1], list(zip(map(
        lambda x: x.text, soup.findAll('td')[::8]), map(lambda x: x.text, soup.findAll('td')[1::8]))))))}

    return proxy['https']


def chrome_webdriver():
    try:
        PROXY = proxy_generator()  # IP:PORT or HOST:PORT
        print('proxy:', PROXY)

        firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
        firefox_capabilities['marionette'] = True

        firefox_capabilities['proxy'] = {
            "proxyType": "MANUAL",
            "httpProxy": PROXY,
            "sslProxy": PROXY
        }
        firefox_capabilities["pageLoadStrategy"] = "eager"
        cookie = 'AQEDATe-csACVLx3AAABfAolGqsAAAF8LjGeq00AOqY34TIfcMpo0GMSXwwReRXp8gKoSsgxI97st5e4FDlO4VK3DSXXOevyluAtGlk60gX6PwXLDBC_9WEviRb8xyLb9vutyfrzfaji_5hPevzVoRdU'
        firefox_capabilities['acceptSslCerts'] = True
        chrome = webdriver.Firefox(capabilities=firefox_capabilities)
        chrome.set_page_load_timeout(20)
        chrome.get("http://api.ipify.org")
        chrome.set_page_load_timeout(60)
        chrome.get('https://www.linkedin.com')
        chrome.add_cookie({
            'name': 'li_at',
            'value': cookie,
            'domain': '.linkedin.com'
        })
        return chrome
    except Exception as e:
        raise e


def scrape_linkedin(link, chrome):
    try:
        chrome.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
        chrome.get(link)
        time.sleep(15)
        chrome.get(chrome.current_url + 'about')
        start = time.time()
        lastHeight = chrome.execute_script("return document.body.scrollHeight")
        while True:
            chrome.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)
            newHeight = chrome.execute_script(
                "return document.body.scrollHeight")
            if newHeight == lastHeight:
                break
            lastHeight = newHeight
            end = time.time()
            if round(end-start) > 20:
                break

        company_page = chrome.page_source

        linkedin_soup = bs(company_page.encode("utf-8"), 'html.parser')
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
        print('function',jsonOutput)
        return jsonOutput

    except Exception as e:
        chrome.quit()
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
    for document in activeCompanies.find():
        if document.get('linkedin') is not None:
            links.append(
                (document.get('uuid'), document.get('linkedin')['value']))
        else:
            non_linked_in_companies.append(document.get('uuid'))
        # print(len(links))
        if len(links) == 10:
            # print(links)
            while True:
                try:
                    chrome = chrome_webdriver()
                    break
                except Exception as e:
                    print(e)
            for i in links:
                try:
                    print(i)
                    document = activeCompanies.find_one({'uuid': i[0]})
                    if document.get('num_employees_enum') is None:
                        jsonOutput = scrape_linkedin(i[1], chrome)
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
                            size = document.get(
                                'num_employees_enum').split('_')
                            jsonOutput['Company Size'] = str(
                                int(size[1])) + "-" + str(int(size[2])) + " employees"
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
            chrome.quit()
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
                        size = document.get('num_employees_enum').split('_')
                        jsonOutput['Company Size'] = str(
                            int(size[1])) + "-" + str(int(size[2])) + " employees"
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
