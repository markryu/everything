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

def try_each_proxy(each_page, proxy):
    print ('Using proxy: ', proxy)
    page = requests.get(each_page, proxies={"http": proxy, "https": proxy})
    soup = bs(page.content, 'html.parser')
    each_page_with_links = soup.find_all('div',{'class':'company g_0'})
    return each_page_with_links


def get_all_city_links(industry):
    cities = ['manila', 'quezon-city', 'taguig']
    base_url  = 'https://www.businesslist.ph/category/'
    link_for_each_city = []
    all_pages = []
    done = False
    proxies = get_proxies(500)
    for city in cities:
        link_for_each_city.append(base_url + industry + '/city:' + city +'/')
    for each_city in link_for_each_city:
        while done == False:
            proxy = random.choice(proxies)
            try:
                page = requests.get(each_city, proxies={"http": proxy, "https": proxy})
                soup = bs(page.content, 'html.parser')
                text_in_page = soup.find('div', {'class':'pages_container_top'}).text
                number_in_text = ''
                for letters in text_in_page:
                    if letters in ['0','1','2','3','4','5','6','7','8','9']:
                        number_in_text += letters
                number_of_results = int(number_in_text)
                number_of_pages = int(np.ceil(number_of_results / 20))
                print ('Total number of Pages are: ', number_of_pages)
                for every in range(1,number_of_pages+1):
                    all_pages.append(each_city + str(every))
                done = True
            except:
                print ("Retrying...")
                proxy = random.choice(proxies)
    return all_pages


def link_get(count, list_of_pages, industry):
    all_links = []
    for each_page in list_of_pages:
        finished = False
        while finished == False:
            proxies = get_proxies(500)
            proxy = random.choice(proxies)
            try:
                each_page_with_links = try_each_proxy(each_page, proxy)
                base_url = 'https://www.businesslist.ph'
                for links in each_page_with_links:
                    link = base_url + (links.find('a').get('href'))
                    all_links.append(link)
                    finished = True
            except:
                print ('Failed: Trying another proxy.')
        df = pd.DataFrame(all_links, columns=["column"])
        count += 1
        print ('Scrape Successful.... Adding to CSV.')
        if count == 1:
            df.to_csv(industry + '.csv', index=False)
        else:
            with open(industry + '.csv', 'a') as f:
                df.to_csv(f, header=False, index = False)
        time.sleep(2)
        print (count, ": DONE")
    return count

industry = input('Enter the industry extension from url: ')
continue_from_csv = input('Continue from CSV? y/n: ')
if continue_from_csv.lower() == 'y':
    index_number = eval(input("(\n Use last added to csv number from last run.\nStart from 0 if not sure.\nRow Number from csv file: "))
    index_number = index_number - 1
else:
    index_number = 0

print (f'\n Starting to scrape {industry} from www.businesslist.ph \n')
identifier = False
while identifier == False:
    if continue_from_csv.lower() == "y":
        df = pd.read_csv(f"{industry}-city-links.csv")
        list_of_pages = df["links"][index_number:]
        link_get(index_number, list_of_pages, industry)
        identifier = True

    elif continue_from_csv.lower() == "n":
        list_of_pages = get_all_city_links(industry)
        df = pd.DataFrame({"links":list_of_pages})
        df.to_csv(f"{industry}-city-links.csv", index=False)
        link_get(0, list_of_pages, industry)
        identifier = True

    else:
        ("Wrong input, try again.")
        break

df = pd.read_csv(f'{industry}.csv')
df = df.drop_duplicates()
df.to_csv(industry + '-duplicates-dropped.csv', index=False)

if os.path.exists(f"{industry}.csv"):
    os.remove(f"{industry}.csv")
    print (f"{industry}.csv is now removed.")
else:
    print (f"{industry}.csv already removed.")

if os.path.exists(f"{industry}-city-links.csv"):
    os.remove(f"{industry}-city-links.csv")
    print (f"{industry}-city-links.csv is now removed.")
else:
    print (f"{industry}-city-links.csv is already removed.")

print (f'\nFirst part of the scraping is done, you can continue the second part.\n')
print ("Press any key to exit.")
input()