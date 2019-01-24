#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib
import urllib2
import json
from bs4 import BeautifulSoup
import constant

def film_info(title,year):
    #print title
    #print year
    info = title+constant.tab+year+constant.tab
    imdbID = ""
    #req_mojo_url = "http://www.omdbapi.com/?plot=short&r=json&tomatoes=true&t="
    #film_t = "+".join(title.split(" "))
    #print film_t
    #req_mojo_url = req_mojo_url + title + "&y=" + year
    #print req_mojo_url
    req_mojo_url = "http://www.omdbapi.com/?"
    data_by_title = {"plot":"full","r":"json","tomatoes":"true","type":"movie","t":title,"y":year}
    req_mojo_by_title_url = req_mojo_url + urllib.urlencode(data_by_title)
    print req_mojo_by_title_url
    r = urllib2.urlopen(req_mojo_by_title_url).read()
    mojo_return = json.loads(r)
    if(mojo_return["Response"] == "False"):
        data_by_search = {"r":"json","type":"movie","s":title,"y":year,'page':1}
        req_mojo_by_search_url = req_mojo_url + urllib.urlencode(data_by_search)
        print req_mojo_by_search_url
        r = urllib2.urlopen(req_mojo_by_search_url).read()
        mojo_return = json.loads(r)
        print r
        if(mojo_return["Response"] == "False"):
            second_req_url = req_mojo_url + urllib.urlencode({"plot":"full","r":"json","tomatoes":"true","type":"movie","t":title})
            print second_req_url
        else:
            imdbID = mojo_return["Search"][0]["imdbID"]
            second_req_url = req_mojo_url + urllib.urlencode({"plot":"full","r":"json","tomatoes":"true","type":"movie","i":imdbID})
        r_by_ID = urllib2.urlopen(second_req_url).read()
        mojo_return = json.loads(r_by_ID)
        info = info + mojo_return["imdbRating"] + constant.tab + mojo_return["imdbVotes"] + constant.tab + mojo_return["tomatoMeter"] + constant.tab + mojo_return["tomatoRating"] + constant.tab + mojo_return["tomatoReviews"] + constant.tab 
    else:
        info = info + mojo_return["imdbRating"] + constant.tab + mojo_return["imdbVotes"] + constant.tab + mojo_return["tomatoMeter"] + constant.tab + mojo_return["tomatoRating"] + constant.tab + mojo_return["tomatoReviews"] + constant.tab 
        imdbID = mojo_return["imdbID"]
    req_douban_url = "https://api.douban.com/v2/movie/imdb/" + imdbID
    print req_douban_url
    #print imdbID
    r_douban = urllib2.urlopen(req_douban_url).read()
    douban_return = json.loads(r_douban)
    #print douban_return["rating"]["average"]
    #print str(douban_return["rating"]["numRaters"])+"!"
    info = info + str(douban_return["rating"]["average"]) + constant.tab + str(douban_return["rating"]["numRaters"]) + constant.tab
    print info
    return info
#print film_info("Frequently Asked Questions About Time Travel","2009")
#print film_info("Star Wars: The Force Awakens","2015")
#print film_info("E.T.: The Extra-Terrestrial","1982")
#print film_info("Planet of the Apes","2001")
#print film_info("The Road Warrior","1981")
#print film_info("The Avengers","2012")
def single_genre_film(genre):
    hfile=open(constant.mojo_info_dir+genre+"_film_info_list","rb")
    lines = hfile.readlines()
    wfile = open(constant.mojo_info_dir+"score_"+genre,"wb")
    for tmp_line in lines:
        line = tmp_line.strip().split("	")
        single_film_info = film_info(line[0].split("(")[0].strip(),line[2].split(",")[1].strip())+"\n"
        wfile.write(single_film_info)
    wfile.close()
#for i in range(0,constant.web_num):
#    genre = constant.genres[i]
#    print genre
#    single_genre_film(genre)
single_genre_film(constant.genres[7])
#print "avatar (2001)".split("(")[0].strip()