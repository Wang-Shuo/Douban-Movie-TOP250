'''
This module gets the detail information by parsing single website of every movie, including actors, director, year informations and so on.
'''

from bs4 import BeautifulSoup
import requests
import re
import pandas
import time
import random

film_list = []

link = []

def get_info(film_link):
    r1 = requests.get(film_link)
    c1 = r1.content
    full_page = BeautifulSoup(c1, "html.parser")

    film_info = {}

    try:
        full_content = full_page.select("#content")[0]
    except:
        return {
                "title": None, "year": None, "director": None, "screenwriter": None,
                "actor_1": None, "actor_2": None, "actor_3": None, "genre_1": None, "genre_2": None,
               "country": None, "runtime": None, "imdb_link": None, "rating_score": None, "rating_people": None,
               "star5": None, "star4": None
                }

    film_info["title"] = full_content.find("span", {"property": "v:itemreviewed"}).text
    film_info["year"] = full_content.find("span", {"class": "year"}).text.split('(')[1].split(')')[0]

    # the whole content we are interested in scraping
    coi = full_content.find("div", {"class": "subjectwrap clearfix"})

    # the main content about the film
    coi_1 = coi.find("div", {"id": "info"})

    # the ratings of film from users
    coi_2 = coi.find("div", {"class": "rating_wrap clearbox"})

    try:
        film_info["director"] = coi_1.select("span .attrs")[0].find('a').text
    except:
        film_info["director"] = None

    try:
        film_info["screenwriter"] = coi_1.select("span .attrs")[1].find('a').text
    except:
        film_info["screenwriter"] = None

    try:
        film_info["actor_1"] = coi_1.find("span", {"class": "actor"}).find_all('a')[0].text
        film_info["actor_2"] = coi_1.find("span", {"class": "actor"}).find_all('a')[1].text
        film_info["actor_3"] = coi_1.find("span", {"class": "actor"}).find_all('a')[2].text
    except:
        film_info["actor_3"] = None

    try:
        film_info["genre_1"] = coi_1.find_all("span", {"property":"v:genre"})[0].text
        film_info["genre_2"] = coi_1.find_all("span", {"property":"v:genre"})[1].text
    except:
        film_info["genre_2"] = None

    film_info["country"] = coi_1.text.split('\n')[5].split(':')[1].replace(" ", "")

    try:
        film_info["runtime"] = coi_1.find("span", {"property":"v:runtime"}).text
    except:
        film_info["runtime"] = None

    try:
        film_info["imdb_link"] = coi_1.find('a', {"rel": "nofollow"}).get('href')
    except:
        film_info["imdb_link"] = None

    try:
        film_info["rating_score"] = coi_2.find("strong", {"class": "ll rating_num"}).text
    except:
        film_info["rating_score"] = None

    try:
        film_info["rating_people"] = coi_2.find("span", {"property": "v:votes"}).text
    except:
        film_info["rating_people"] = None

    try:
        film_info["star5"] = coi_2.select(".rating_per")[0].text
    except:
        film_info["star5"] = None

    try:
        film_info["star4"] = coi_2.select(".rating_per")[1].text
    except:
        film_info["star4"] = None

    return film_info


for page_index in range(0,250,25):
    url = "https://movie.douban.com/top250?start={}&filter=".format(str(page_index))
    r = requests.get(url)
    print(r.status_code)
    c = r.content
    full_page = BeautifulSoup(c, "html.parser")

    items = full_page.find_all("ol", {"class": "grid_view"})[0].find_all("li")
    #items = content.select(".grid_view")[0].find_all("li")

    for item in items:
        film_link = item.find_all('a')[0].get('href')
        link.append(film_link)
        film_info = get_info(film_link)
        film_list.append(film_info)
        time.sleep(2+random.random())


film_df = pandas.DataFrame(film_list)

film_df.to_csv("top250_detail.csv")
