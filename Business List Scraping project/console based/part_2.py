import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import requests
from lxml.html import fromstring
import requests
import random
import time
import numpy as np
import os

def get_proxies(number):
    free_proxy_urls= ['https://www.us-proxy.org/', 'https://free-proxy-list.net/']
    proxy_list = list()
    for every_url in free_proxy_urls:
        source = requests.get(every_url)
        parser = fromstring(source.text)
        for i in parser.xpath('//tbody/tr')[:number]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxy_list.append(proxy)
    return proxy_list

title = input("Enter the filename without csv extension: ")
continue_from_csv = input("Continue from csv? y/n: ")
if continue_from_csv.lower() == 'y':
    continue_from = eval(input("(Check csv file for row number)\nEnter Row to Start from: "))
    continue_from = continue_from - 1
else:
    continue_from = 0
df = pd.read_csv(f"{title}-duplicates-dropped.csv")

proxies =get_proxies(500)
proxy = np.random.choice(proxies)
for each_url in df.column[continue_from:]:
    name = 'None'
    weblinks = 'None'
    telephone = 'None'
    mobile = 'None'
    number_of_employees = 'None'
    contact = 'None' 
    fax = 'None' 
    manager = 'None'
    finished = False
    none_indicator = True
    number_of_tries = 1
    while none_indicator == True:
        try:
            url = each_url
            print ('Trying Proxy: ', proxy)
            page = requests.get(url, proxies={"http": proxy, "https": proxy})
            soup = bs(page.content, 'html.parser')
            all_texts = soup.find_all('div', {'class':'label'})
            #print("Process time is: ", time.process_time())
            try:
                name = soup.find('span', {'id':'company_name'}).text
            except:
                name = 'None'
            try:
                weblinks = soup.find("div", class_= "text weblinks").text
            except:
                weblinks = 'None'
            try:
                address = soup.find('div',{'class':'text location'}).text
            except:
                address = 'None'    
            try:
                telephone = soup.find('div',{'class':'text phone'}).text
            except:
                telephone = 'None'    
            try:
                for each in all_texts:
                    if each.text == 'Mobile phone':
                        mobile = each.find_next().contents[0]
            except:
                mobile = 'None'
            try:
                for each in all_texts:
                    if each.text == 'Employees':
                        number_of_employees = each.find_next().contents[0]
            except:
                number_of_employees = 'None'
            try:
                for each in all_texts:
                    if each.text == 'Contact Person':
                        contact = each.find_next().contents[0]
            except:
                contact = 'None'
            try:
                for each in all_texts:
                    if each.text == 'Fax':
                        fax = each.find_next().contents[0]
                number_of_tries = 0
            except:
                fax = 'None'
            try:
                for each in all_texts:
                    if each.text == 'Company manager':
                        manager = each.find_next().contents[0]
                number_of_tries = 0
            except:
                manager = 'None'

            finished = True
            print ('Tried: ', continue_from, ' ',each_url)
        except:
            print ('Trying another proxy...')
            print ()
            number_of_tries += 1
            print ("No. of Tries: ", number_of_tries)
        if name == 'None':
            proxy = np.random.choice(proxies)
        else:
            none_indicator = False
            continue_from += 1
    else:
        print ('This is the scraped link: ', weblinks, ';') 
        time.sleep(2)
        df_1 = pd.DataFrame.from_dict({'company_name':[name], 'address':[address], 'website':[weblinks], 'telephone_no':[telephone], 'mobile_phone':[mobile], 'no._of_employees':[number_of_employees], 'contact_person':[contact], 'fax':[fax], 'company_manager':[manager]})
        if continue_from == 1:
            print (continue_from, ': done.', ';')
            df_1.to_csv(f"{title}-done.csv", index = False, encoding="utf-8")
            print ()
        else:
            print (continue_from, ': done.', ';')
            with open(f"{title}-done.csv", 'a',  encoding="utf-8") as f:
                df_1.to_csv(f, header=False, index = False)

if os.path.exists(f"{title}-done.csv"):
    os.remove(f"{title}-done.csv")
    print (f"{title}-done.csv is now removed.")
else:
    print (f"{title}-title.csv already removed.")

print ('\nThe program is done')
print ('Press any key to exit')
input()