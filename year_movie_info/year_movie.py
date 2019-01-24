#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import urllib2
from bs4 import BeautifulSoup
import constant
max_year = 2015
min_year = 2006
#min_year = 2006
data_file_suffix = "year_info"
per_year_url_prefix = "http://www.boxofficemojo.com/yearly/chart/?yr="
per_year_url_suffix = "&p=.htm"
TAB = "	"
SPECIAL = " "+TAB
special_str_soup = BeautifulSoup(open(constant.special_str_html, "rb"))
blank_str = special_str_soup.find_all("div",class_="blank")[0].text.encode("utf-8") + " " + "	"
def single_film_info(single_film_url):
    film_info = ""
    content = urllib2.urlopen(constant.web_host+single_film_url).read()
    csoup = BeautifulSoup(content)
    mp_box_tab_tags = csoup.find_all('div', class_="mp_box_tab")
    mp_box_content_tags = csoup.find_all('div', class_="mp_box_content")
    info_list = ["N/A"+TAB,"N/A"+TAB+"N/A"+TAB+"N/A"+TAB, "N/A"+TAB+"N/A"+TAB+"N/A"+TAB, "N/A"+TAB]
    center_tag = csoup.find_all('center')[0]
    #print center_tag
    td_tags = center_tag.find_all("td")
    #print len(td_tags)
    if(len(td_tags) >= 6):
        b_tags = center_tag.find_all("b")
        info_list[3] = b_tags[len(b_tags)-1].text.encode("utf-8").strip(blank_str)+TAB
    #print info_list[3]
    for i in range(0, len(mp_box_tab_tags)):
        tab_str = mp_box_tab_tags[i].text.encode("utf-8").strip(blank_str)
        if tab_str == "The Players":
            player_list = ["N/A"+TAB,"N/A"+TAB+"N/A"+TAB+"N/A"+TAB]
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
                        player_list[0] = tmp_row_name_str + TAB
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
                        player_list[0] = player_list[0].split(',')[0] + TAB
                if(player_row_kind == "Actors:" or player_row_kind == "Actor:"):
                    player_row = player_row.find_next_sibling()
                    player_brs = player_row.find_all("br")
                    tmp_row_name_str = player_row.text.encode("utf-8").strip(blank_str)
                    br_num = len(player_brs)
                    if(br_num == 0):
                        player_list[1] = tmp_row_name_str + TAB+"N/A"+TAB+"N/A"+TAB
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
                        #print player_list[1]
                        tmp_list = player_list[1].split(",")
                        tmp_list_len = len(tmp_list)
                        #print tmp_list
                        if(tmp_list_len >= 3):
                            player_list[1] = tmp_list[0].strip(SPECIAL)+TAB+tmp_list[1].strip(SPECIAL)+TAB+tmp_list[2].strip(SPECIAL)+TAB
                        elif(tmp_list_len == 2):
                            player_list[1] = tmp_list[0].strip(SPECIAL)+TAB+tmp_list[1].strip(SPECIAL)+TAB+"N/A"+TAB
                        elif(tmp_list_len < 2):
                            player_list[1] = tmp_list[0].strip(SPECIAL)+TAB+"N/A"+TAB+"N/A"+TAB
                player_row = player_row.find_next_sibling()
            info_list[0] = player_list[0]
            info_list[1] = player_list[1]
            #print info_list[1]
            continue
        if(tab_str == "Genres"):
            td_tags = mp_box_content_tags[i].find_all("td")
            td_tag_num = len(td_tags)
            sf_index = 0
            info_list[2] = ""
            for j in range(0,td_tag_num):
                if(sf_index == 3):
                    break;
                td_tag_title = td_tags[j].text.encode("utf-8").strip(blank_str)
                if(td_tag_title.find("Sci-Fi") > -1 and td_tag_title.find("Animation") == -1):
                    info_list[2] = info_list[2] + td_tag_title.strip(SPECIAL) + TAB
                    sf_index += 1
            if(sf_index < 3):
                for j in range(0,td_tag_num):
                    if(sf_index == 3):
                        break
                    if(j % 2 == 1):
                        continue
                    td_tag_title = td_tags[j].text.encode("utf-8").strip(blank_str)
                    if(td_tag_title.find("Sci-Fi") == -1):
                        info_list[2] = info_list[2] + td_tag_title.strip(SPECIAL) + TAB
                        sf_index += 1
            if(sf_index == 2):
                info_list[2] = info_list[2] + "N/A" + TAB
            elif(sf_index == 1):
                info_list[2] = info_list[2] + "N/A" + TAB + "N/A" + TAB
            elif(sf_index < 1):
                info_list[2] = "N/A" + TAB + "N/A" + TAB + "N/A" + TAB
    #print info_list
    for info in info_list:
        film_info = film_info + info
    return film_info
#print single_film_info("/movies/?id=revenant.htm")
def single_year_info(year):
    year_url = per_year_url_prefix + str(year) + per_year_url_suffix
    content = urllib2.urlopen(year_url).read()
    csoup = BeautifulSoup(content)
    tbs = csoup.find_all("table")
    trs = tbs[6].find_all("tr")
    yfile = open(str(year)+"_info", "w")
    for i in range(2,32):
        film_info = str(i-1) + TAB
        #atags = trs[i].find_all("a")
        #print atags[0].text
        #film_info = film_info + atags[0].text.encode("utf-8") + TAB + single_film_info(atags[0]['href']) + "\n"
        btags = trs[i].find_all("b")
        print btags[1]
        film_info = film_info + btags[1].text.encode("utf-8").strip(blank_str)+TAB+"\n"
        yfile.write(film_info)
        #print trs[i]
    yfile.close()
    #hfile = open("raw_html","w")
    #hfile.write(tbs[6].prettify())
    #hfile.close()
#single_year_info(2015)
for year in range(min_year,max_year):
    print year
    single_year_info(year)