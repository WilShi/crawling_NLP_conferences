import re
import sys
import requests
import pandas as pd
from bs4 import BeautifulSoup

csv_file_list = []
total_name_list = []

def make_soup(url):
    """
    Use requests and BeautifulSoup 4 library to turn the parameter 
    URL into and return HTML code in BeautifulSoup format.
    """
    html = requests.get(url) #Creat html file by url
    html.encoding = 'utf-8'
    soup = BeautifulSoup(html.text, 'html5lib')
    return soup

def get_link(soup, conf): 
    """
    Use parameter soup and conference's name find and return all earlier 
    conference websites.
    """
    links = []
    if soup.find_all('tr') != []:
        for trtag in soup.find_all('tr'):
            if trtag.find_all('th')[0].text == conf:
                for tdtag in trtag.find_all('td'):
                    if tdtag.find_all('a') != []:
                        links.append(tdtag.find_all('a')[0].get('href'))
                # print(conf)
                # print(links)
    return links

def get_name(link):
    """
    Use the parameter link to create csv file for all the names and information 
    in the URL page
    """
    soup = make_soup(link)
    name_list = []
    gender = []
    race = []
    conf_name = re.findall('[A-Za-z\-]{2,6}\d{4}', link)[0]
    for ptag in soup.find_all('p', class_='d-sm-flex'):
        for spantag in ptag.find_all('span'):
            if spantag.find_all('strong'):
                paper = spantag.find_all('strong')[0]
                for name in spantag.find_all('a'):
                    if name.text != paper.text:
                        name_list.append(name.text)
                        total_name_list.append(name.text)
                        gender.append('')
                        race.append('')
                        # print(name.text)
    print("Create file: ", conf_name)
    print("File size: ", len(name_list))
    conf_name += '.csv'
    csv_file_list.append(conf_name)
    csv_file = pd.DataFrame({'Name':name_list,'Gender':gender,'Race':race})
    csv_file.to_csv(conf_name, index=False, sep=',')
    return None

def crawl_site(url, links):
    """
    Use the parameter url and list of links find all links between 2020 to 2010
    and call get_name to crawl names.
    """
    url = url[:url.find('/a')]
    for link in links:
        link = url + link
        if int(re.findall('\d{4}', link)[0]) > 2009:
            get_name(link)
    return None

if __name__ == '__main__':
    url = "https://www.aclweb.org/anthology/"
    soup = make_soup(url)
    confs = ['ACL', 'EMNLP', 'NAACL']
    for conf in confs:
        links = get_link(soup, conf)
        crawl_site(url, links)
    # links = get_link(soup, confs[2])
    # crawl_site(url, links)

    f = open('csv_list.txt', 'w')
    for file in csv_file_list:
        f.write(file)
        f.write('\n')
    f.close()

    f = open('total_name_list.txt', 'w')
    for name in total_name_list:
        f.write(name)
        f.write('\n')
    f.close()