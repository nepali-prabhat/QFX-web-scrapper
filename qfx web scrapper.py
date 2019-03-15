# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq

my_url = 'http://www.qfxcinemas.com'
#opening connection, grabbing the page
uClient = uReq(my_url)
page_html = uClient.read()
uClient.close()
#converting the raw html with bs
page_soup = soup(page_html, 'html.parser')
movies =  page_soup.find_all('div','movies')
qfx = {}
#movie_status = 0 for now showing and 1 for comming movies
def make_data(movie_status):
    movie_posters = movies[movie_status%2].find_all("div","movie-poster")
    detail_url_objects_list = []
    ticket_url_objects_list = []
    for movie_poster in movie_posters:
        a_in_movie_poster = movie_poster.find_all("a")
        detail_url_objects_list.append(a_in_movie_poster[0])
        if len(a_in_movie_poster) == 2 and movie_status == 0:
            ticket_url_objects_list.append(a_in_movie_poster[1])
    detail_url = [my_url+url["href"] for url in detail_url_objects_list]
    ticket_url = [my_url+url["href"] for url in ticket_url_objects_list]
    now_showing = []
    for index, url in enumerate(detail_url):
        uClient = uReq(url)
        each_movie_html = uClient.read()
        uClient.close()
        movie_soup = soup(each_movie_html,'html.parser')
        movie_title = movie_soup.body.find_all("h3",{"class":'movie-title'})[0].string
        movie_info_tuple = [("title",movie_title)]
        
        movie_info_p = movie_soup.body.find_all("div",{"class":'movie-info'})[0].find_all('p')
        movie_info_tuple = movie_info_tuple + [(p.find_all('span')[0].string.replace(":",""), p.find_all('span')[1].string) for p in movie_info_p]
        if movie_status==0:
            movie_info_tuple.append(("ticket",ticket_url[index]))
        now_showing.append(dict(movie_info_tuple))
    return now_showing

qfx["now_showing"] = make_data(0)
qfx["comming_soon"] = make_data(1)

import datetime
now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")

import json

with open("./qfx-movie-"+date+".json", 'w') as fp:
    json.dump(qfx,fp)