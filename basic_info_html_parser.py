#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib2
from bs4 import BeautifulSoup
import constant

special_str_soup = BeautifulSoup(open(constant.special_str_html, "rb"))
blank_str = special_str_soup.find_all("div",class_="blank")[0].text.encode("utf-8") + " " + "	"

def web_spider_film_list(url, data_file_name):
    hfile = open(data_file_name,"wb")

    content = urllib2.urlopen(url).read()
    #content = open("test.html","rb")
    soup = BeautifulSoup(content)
    tables = soup.find_all("table")
    tag_class_type = type(tables[0])
    print tag_class_type
    #print type(soup)
    #print tables[3]
    index_row = 0
    for child in tables[3].children:
        #print child
        if index_row == 0:
            index_row += 1
            continue
        index_col = 0
        for cc in child:
            if(tag_class_type == type(cc)):
                index_col += 1
                tmp_str = cc.text.encode('utf8')+'	'
                if index_col == 8: tmp_str += '\n'
                hfile.write(tmp_str)
    #hfile.write(tables[3].text)
    #hfile.write(soup.prettify().encode('utf8'))
    hfile.close()

#for i in range(0,constant.web_num):
#	web_spider_film_list(constant.web_urls[i], "./mojo_genres/"+constant.genres[i])

def web_spider_single_film_info(url):
    print url
    film_info = u''.encode("utf-8")
    content = urllib2.urlopen(url).read()
    #test_w = open("test_predator","wb")
    soup = BeautifulSoup(content,"html.parser")
    #test_w.write(soup.prettify().encode("utf-8"))
    #center info
    release_date = "N/A"
    center_tag = soup.find_all('center')[0]
    td_tags = center_tag.find_all("td")
    #print td_tags
    td_tag_num = len(td_tags)
    #print td_tag_num
    start_td_index = 1
    if(td_tag_num == 6):
        start_td_index = 0
    for i in range(start_td_index,td_tag_num):
        #print i
        if td_tags[i].b:
            film_info = film_info + td_tags[i].b.text.encode("utf-8").strip(blank_str) + "	"
            if i == 2:
                release_date = td_tags[i].b.text.encode("utf-8").strip(blank_str)
                #print release_date
    
    mp_box_tab_tags = soup.find_all('div', class_="mp_box_tab")
    mp_box_content_tags = soup.find_all('div', class_="mp_box_content")
    #tbody_tags = soup.find_all('table')
    #print tbody_tags
    #6 info : office box, opening weekend, director actor, Academy Award, Genres
    info_list = ["N/A	N/A	N/A	N/A	N/A	","N/A	N/A	N/A	","N/A	N/A	","N/A	0	0	","N/A	"]
    for i in range(0, len(mp_box_tab_tags)):
        tab_str = mp_box_tab_tags[i].text.encode("utf-8").strip(blank_str)
        #print tab_str
        if tab_str == "Total Lifetime Grosses":
            tr_tags = mp_box_content_tags[i].find_all("tr")
            tr_num = len(tr_tags)
            if tr_num == 4:
                td_tags = mp_box_content_tags[i].find_all("td")
                info_list[0] = td_tags[1].text.encode("utf-8").strip(blank_str) + "	" + td_tags[2].text.encode("utf-8").strip(blank_str) + "	" + td_tags[4].text.encode("utf-8").strip(blank_str) + "	" + td_tags[5].text.encode("utf-8").strip(blank_str) + "	" + td_tags[8].text.encode("utf-8").strip(blank_str) + "	"
            elif tr_num == 1:
                td_tags = mp_box_content_tags[i].find_all("td")
                box_num = td_tags[1].text.encode("utf-8").strip(blank_str)
                if td_tags[0].text == "Domestic:":
                    info_list[0] = box_num + "	N/A	N/A	N/A	N/A	" 
                else:
                    info_list[0] = "N/A	N/A	" + box_num + "	N/A	N/A	"
            continue
        if tab_str == "Domestic Summary":
            td_tags = mp_box_content_tags[i].find_all("td")
            td_tag_title0 = td_tags[0].text.encode("utf-8").strip(blank_str)
            #print td_tag_title0
            if(td_tag_title0 == "Opening"+blank_str[0:2]+"Weekend:"):
                info_list[1] = release_date + "	" +td_tags[1].text.encode("utf-8").strip(blank_str) + "	N/A	"
            elif(td_tag_title0 == "Release"+blank_str[0:2]+"Dates:"):
                info_list[1] = td_tags[1].find_all("b")[1].text.encode("utf-8").strip(blank_str) + "	" + td_tags[6].text.encode("utf-8").strip(blank_str) + "	" + td_tags[3].find_all("b")[0].text.encode("utf-8").strip(blank_str) + "	"
            continue
        if tab_str == "The Players":
            player_list = ["N/A	","N/A	"]
            mp_box_parent = mp_box_tab_tags[i].find_parent().find_parent()
            #print mp_box_parent
            player_row = mp_box_parent.find_next_sibling()
            while player_row and player_row.has_attr("class") == False:
                player_row_kind = player_row.text.encode("utf-8").strip(blank_str)
                if(player_row_kind == "Director:" or player_row_kind == "Directors:"):
                    player_row = player_row.find_next_sibling()
                    player_brs = player_row.find_all("br")
                    #tmp_utext = player_row.text.encode("utf-8")
                    #print type(player_row.text)
                    tmp_row_name_str = player_row.text.encode("utf-8").strip(blank_str)
                    #print tmp_row_name_str
                    br_num = len(player_brs)
                    if(br_num == 0):
                        player_list[0] = tmp_row_name_str + "	"
                    else:
                        #print player_brs
                        index_range = range(0,br_num-1)[::-1]
                        tmp_short_name_str = player_brs[br_num-1].text.encode("utf-8")
                        player_list[0] = tmp_short_name_str + "	"
                        for i in index_range:
                            tmp_long_name_str = player_brs[i].text.encode("utf-8")
                            player_list[0] = tmp_long_name_str[0:tmp_long_name_str.find(tmp_short_name_str)] + "," +player_list[0]
                            tmp_short_name_str = tmp_long_name_str
                        player_list[0] = tmp_row_name_str[0:tmp_row_name_str.find(tmp_short_name_str)] + "," +player_list[0]
                if(player_row_kind == "Actors:" or player_row_kind == "Actor:"):
                    player_row = player_row.find_next_sibling()
                    player_brs = player_row.find_all("br")
                    tmp_row_name_str = player_row.text.encode("utf-8").strip(blank_str)
                    br_num = len(player_brs)
                    if(br_num == 0):
                        player_list[1] = tmp_row_name_str + "	"
                    else:
                        #print player_brs
                        index_range = range(0,br_num-1)[::-1]
                        tmp_short_name_str = player_brs[br_num-1].text.encode("utf-8").strip(blank_str)
                        player_list[1] = tmp_short_name_str + "	"
                        for j in index_range:
                            tmp_long_name_str = player_brs[j].text.encode("utf-8").strip(blank_str)
                            player_list[1] = tmp_long_name_str[0:tmp_long_name_str.find(tmp_short_name_str)] + "," +player_list[1]
                            tmp_short_name_str = tmp_long_name_str
                        player_list[1] = tmp_row_name_str[0:tmp_row_name_str.find(tmp_short_name_str)] + "," +player_list[1]
                player_row = player_row.find_next_sibling()
            info_list[2] = player_list[0] + player_list[1]
            continue
        if(tab_str.find("Academy Awards") > -1):
            awards_content = urllib2.urlopen(constant.web_host + mp_box_content_tags[i].find_all("a")[0]["href"]).read()
            awards_soup = BeautifulSoup(awards_content,"html")
            #test_w = open("test_award","wb")
            #test_w.write(awards_soup.prettify().encode("utf-8"))
            b_tags = awards_soup.find_all("h3")[0].find_parent().find_all("b")
            b_tags_num = len(b_tags)
            index_b = 0
            for j in range(0, b_tags_num):
                if b_tags[j].a:
                    if j == 0: info_list[3] = b_tags[j].a.text.encode("utf-8").strip(blank_str)
                    elif j > 0: info_list[3] = info_list[3] + "," + b_tags[j].a.text.encode("utf-8").strip(blank_str)
                else:
                    if(index_b < 2):
                        info_list[3] = info_list[3] + "	" +b_tags[j].text.encode("utf-8").strip(blank_str)
                        index_b += 1
            info_list[3] += "	"
        if(tab_str == "Genres"):
            td_tags = mp_box_content_tags[i].find_all("td")
            td_tag_num = len(td_tags)
            index_td_tag = 0
            for j in range(0,td_tag_num):
                td_tag_title = td_tags[j].text.encode("utf-8").strip(blank_str)
                if(td_tag_title.find("Sci-Fi") > -1 and td_tag_title.find("Animation") == -1):
                    if index_td_tag == 0:
                        info_list[4] = td_tag_title + ":" + td_tags[j+1].text.encode("utf-8").strip(blank_str)
                    else:
                        info_list[4] = info_list[4] + "," + td_tag_title + ":" + td_tags[j+1].text.encode("utf-8").strip(blank_str)
                    index_td_tag += 1
                elif td_tag_title.find("Animation") > -1:
                    return ""
            info_list[4] += "	"
    #print info_list
    for i in range(0,5):
        #print type(info_list[i])
        #print type(film_info)
        film_info += info_list[i]
    return film_info
#print web_spider_single_film_info("http://www.boxofficemojo.com/movies/?id=frequentlyaskedquestionsabouttimetravel.htm")
#print web_spider_single_film_info("http://www.boxofficemojo.com/movies/?id=iamlegend.htm")
#print web_spider_single_film_info("http://www.boxofficemojo.com/movies/?id=humansvszombies.htm")
#print web_spider_single_film_info("http://www.boxofficemojo.com/movies/?id=purification.htm")
#print web_spider_single_film_info("http://www.boxofficemojo.com/movies/?id=darkawakening.htm")
#print web_spider_single_film_info("http://www.boxofficemojo.com/movies/?id=starwars7.htm")
#print web_spider_single_film_info("http://www.boxofficemojo.com/movies/?id=monsters2.htm")
#print web_spider_single_film_info("http://www.boxofficemojo.com/movies/?id=plutonash.htm")
#print web_spider_single_film_info("http://www.boxofficemojo.com/movies/?id=timechanger.htm")
def web_spider_film_info(url,data_file_name):
    hfile = open(data_file_name, "wb")
    content = urllib2.urlopen(url).read()
    soup = BeautifulSoup(content)
    tables = soup.find_all("table")
    tag_class_type = type(tables[0])
    index_row = 0
    for child in tables[3].children:
        if index_row == 0:
            index_row += 1
            continue
        index_col = 0
        for cc in child:
            if(tag_class_type == type(cc)):
                index_col += 1
                if(index_col == 2):
                    if type(cc.a) == tag_class_type:
                        single_film_name = cc.text.encode('utf8')
                        single_film_url = cc.a['href']
                        single_film_info = web_spider_single_film_info(constant.web_host + single_film_url)
                        if(len(single_film_info) > 0):
                            hfile.write(single_film_name + '	' + single_film_info +'\n')
                        break
for i in range(0,constant.web_num):
    print constant.genres[i]
    web_spider_film_info(constant.web_urls[i], "./mojo_film_info/" + constant.genres[i] + "_film_info_list")
#web_spider_film_info(constant.web_urls[0], "./mojo_film_info/" + constant.genres[0] + "_film_info_list")