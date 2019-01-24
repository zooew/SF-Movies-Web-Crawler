#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib2
from bs4 import BeautifulSoup
import constant

#special_str_soup = BeautifulSoup(open(constant.special_str_html, "rb"))
#blank_str = special_str_soup.find_all("div",class_="blank")[0].text.encode("utf-8") + " " + "	"
def get_worldwide_box_office(file,url):
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    #hfile = open("single_year_box_office_html","wb")
    #hfile.write(soup.prettify().encode("utf-8"))
    #hfile.close()
    tr_tags = soup.find_all("tr")
    tr_index = 0
    #print tr_tags[0]
    #print tr_tags[1]
    #print tr_tags[2]
    #print tr_tags[3]
    #print tr_tags[4]
    #print tr_tags[5]
    #print tr_tags[-2]
    #print tr_tags[-1]
    tr_num = len(tr_tags)
    movies_num = tr_tags[-2].find_all("td")[0].text.encode("utf-8")
    print movies_num
    #print tr_num-6
    hfile_single_web = open(file,"wb")
    for i in range(5,tr_num-1):
        #print tr.text.encode("utf-8")
        td = tr_tags[i].find_all("td")[3].text.encode("utf-8")
        
        hfile_single_web.write(td+"\n")
    hfile_single_web.close()
get_worldwide_box_office("2016","http://www.boxofficemojo.com/yearly/chart/?view2=worldwide&yr=2016&p=.htm")
years = []
def get_urls(url):
    urls = []
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    #hfile = open("box_office_html","wb")
    #hfile.write(soup.prettify().encode("utf-8"))
    #hfile.close()
    tr_tags = soup.find_all("tr")
    index_tr = 0
    for tr in tr_tags:
    	if index_tr < 3:
    	    index_tr += 1
            continue
        a_tags = tr.find_all("a")
        if(len(a_tags) > 0):
            urls.append(constant.web_host+a_tags[0]["href"].encode("utf-8"))
            years.append(a_tags[0].text.encode("utf-8"))
    return urls
#y_urls = get_urls("http://www.boxofficemojo.com/yearly/?view2=worldwide&view=releasedate&p=.htm")
#url_num = len(y_urls)
#for i in range(0,url_num):
#    get_worldwide_box_office(years[i],y_urls[i])