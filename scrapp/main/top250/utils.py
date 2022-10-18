import re
from bs4 import BeautifulSoup
import requests
import json
import re
import os

top250_dir_path = os.path.dirname(os.path.realpath(__file__))


r = requests.get("https://www.imdb.com/chart/top/")
soup = BeautifulSoup(r.content, "html.parser")

BASE_URL = "https://www.imdb.com"
MOVIE_ITEM_LIST = soup.find("tbody", {"class": "lister-list"}).find_all("tr")


def request_detail_page(movie):
    detail_page_link = movie.find("td", {"class": "titleColumn"}).find("a")['href']
    detail = requests.get(BASE_URL + detail_page_link)
    detail_soup = BeautifulSoup(detail.content, "html.parser")
    return detail_soup


def imdb_id_finder(movie):
    imdb_id = movie.find("div", {"class": "wlb_ribbon"})["data-tconst"]
    return imdb_id


def movie_stars_finder(movie_detail_page):
    try:    #movies which have a teaser
        detail_soup = movie_detail_page
        movie_stars = detail_soup.find("body")
        movie_stars = movie_stars.find("div", {"id": "__next"}).find("main", {"role": "main"})
        movie_stars = movie_stars.find("div", {"class": "sc-2a827f80-2 kqTacj"})
        movie_stars = movie_stars.find("div", {"class": "sc-2a827f80-10 fVYbpg"})
        movie_stars = movie_stars.find("div", {"class": "sc-2a827f80-4 bWdgcV"})
        movie_stars = movie_stars.find("div", {"class": "sc-fa02f843-0 fjLeDR"})
    except: #movies which doesnt have teaser (seppuku)
        detail_soup = movie_detail_page
        movie_stars = detail_soup.find("body")
        movie_stars = movie_stars.find("div", {"id": "__next"}).find("main", {"role": "main"})
        movie_stars = movie_stars.find("div", {"class": "sc-2a827f80-6 jXSdID"})
        movie_stars = movie_stars.find("div", {"class": "sc-2a827f80-10 fVYbpg"})
        movie_stars = movie_stars.find("div", {"class": "sc-2a827f80-8 indUzh"})
        movie_stars = movie_stars.find("div", {"class": "sc-fa02f843-0 fjLeDR"})
    movie_stars = movie_stars.find("ul", {"class": "ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt"})
    #sometimes 2 or more class with same name we have to select lastone
    movie_stars = movie_stars.find_all("li", {"class": "ipc-metadata-list__item ipc-metadata-list-item--link"})[-1]
    movie_stars = movie_stars.find("div", {"class": "ipc-metadata-list-item__content-container"})
    movie_stars = movie_stars.find("ul", {"class": "ipc-inline-list ipc-inline-list--show-dividers ipc-inline-list--inline ipc-metadata-list-item__list-content baseAlt"})
    movie_stars = movie_stars.find_all("li", {"class", "ipc-inline-list__item"})

    return movie_stars


def star_actor_imdb_id(star):
    temp = star.find("a")["href"]
    temp = re.split("\?", temp)
    star_actor = temp[0] #/name/nm0000209/
    return star_actor


def brackets_comma_cleaner(argument):
    argument = str(argument)
    argument = re.sub(r'[(,)]', "", argument)
    return argument



def director_finder(movie_detail_page):

    try:    #movies which have teaser
        detail_soup = movie_detail_page
        directors = detail_soup.find("body")
        directors = directors.find("div", {"id": "__next"}).find("main", {"role": "main"})
        directors = directors.find("div", {"class": "sc-2a827f80-2 kqTacj"})
        directors = directors.find("div", {"class": "sc-2a827f80-10 fVYbpg"})
        directors = directors.find("div", {"class": "sc-2a827f80-4 bWdgcV"})
        directors = directors.find("div", {"class": "sc-fa02f843-0 fjLeDR"})
    except: #movies which doesnt have teaser (seppuku)
        detail_soup = movie_detail_page
        directors = detail_soup.find("body")
        directors = directors.find("div", {"id": "__next"}).find("main", {"role": "main"})
        directors = directors.find("div", {"class": "sc-2a827f80-6 jXSdID"})
        directors = directors.find("div", {"class": "sc-2a827f80-10 fVYbpg"})
        directors = directors.find("div", {"class": "sc-2a827f80-8 indUzh"})
        directors = directors.find("div", {"class": "sc-fa02f843-0 fjLeDR"})
    directors = directors.find("ul", {"class": "ipc-metadata-list ipc-metadata-list--dividers-all title-pc-list ipc-metadata-list--baseAlt"})
    director_name = directors.find("li", {"class": "ipc-inline-list__item"}).find("a").text
    temp_imdb_id = directors.find("li", {"class": "ipc-inline-list__item"}).find("a")["href"]

    temp_imdb_id = re.split("\?", temp_imdb_id)
    director_imdb_id = temp_imdb_id[0]

    return director_imdb_id


def genre_finder(movie_detail_page):
    try:
        detail_soup = movie_detail_page
        movie_genres = detail_soup.find("div", {"class": "sc-2a827f80-2 kqTacj"})
        movie_genres = movie_genres.find("div", {"class": "sc-2a827f80-10 fVYbpg"})
        movie_genres = movie_genres.find("div", {"class": "sc-2a827f80-4 bWdgcV"})
        movie_genres = movie_genres.find("div", {"class": "sc-16ede01-8 hXeKyz sc-2a827f80-11 kSXeJ"})
        movie_genres = movie_genres.find("div", {"class": "ipc-chip-list--baseAlt ipc-chip-list sc-16ede01-4 bMBIRz"})
        movie_genres = movie_genres.find("div", {"class": "ipc-chip-list__scroller"})
        movie_genres = movie_genres.find_all("a")
        return movie_genres
    except: #movies which doesnt have trailer
        movie_genres = detail_soup.find("div", {"class": "sc-2a827f80-6 jXSdID"})
        movie_genres = movie_genres.find("div", {"class": "sc-2a827f80-10 fVYbpg"})
        movie_genres = movie_genres.find("div", {"class": "sc-2a827f80-8 indUzh"})
        movie_genres = movie_genres.find("div", {"class": "sc-16ede01-9 bbiYSi sc-2a827f80-11 kSXeJ"})
        movie_genres = movie_genres.find("div", {"class": "ipc-chip-list--baseAlt ipc-chip-list sc-16ede01-5 ggbGKe"})

        movie_genres = movie_genres.find("div", {"class": "ipc-chip-list__scroller"})
        movie_genres = movie_genres.find_all("a")
        return movie_genres
