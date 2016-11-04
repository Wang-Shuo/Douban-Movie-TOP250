'''
This module gets the basic information of every top 250 movie on douban website, including title, quote,the number of rating people and rating score.
'''

from bs4 import BeautifulSoup
import requests
import re
import pandas

film_list = []

for page_index in range(0,250,25):
    url = "https://movie.douban.com/top250?start={}&filter=".format(str(page_index))
    r = requests.get(url)
    c = r.content
    content = BeautifulSoup(c, "html.parser")

    items = content.find_all("ol", {"class": "grid_view"})[0].find_all("li")

    for item in items:
        film_info = {}
        info = item.find_all("div", {"class": "info"})[0]

        title = info.find_all("span", {"class": "title"})[0]

        star = info.find_all("div", {"class": "star"})[0]
        star_score = star.find_all("span", {"class": "rating_num", "property": "v:average"})[0]
        star_num = star.find_all("span")[3]

        try:
            quote = info.find_all("p", {"class": "quote"})[0]
            film_info["quote"] = quote.text.replace("\n","")
        except:
            film_info["quote"] = None

        film_info["title"] = title.text
        film_info["star_score"] = star_score.text
        film_info["star_num"] = re.findall('\d+', star_num.text)[0]


        film_list.append(film_info)

film_df = pandas.DataFrame(film_list)
film_df.to_csv("top250_basic.csv")
