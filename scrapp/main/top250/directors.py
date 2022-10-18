from utils import (
    json,
    request_detail_page,
    MOVIE_ITEM_LIST,
    re
)

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

    director = {}
    director["name"] = director_name
    director["imdb_id"] = director_imdb_id
    return director

def check_director(directors_list, director_id_and_name_dict):
    #very first element cant aappend without this
    if len(directors_list) == 0:
        return True
    else:
        for i in range(len(directors_list)):
            if director_id_and_name_dict["imdb_id"] == directors_list[i]["imdb_id"]:
                return False

        return True

def append_director(directors_list, director_id_and_name_dict):
    directors_list.append({
        "imdb_id"   :   director_id_and_name_dict["imdb_id"],
        "name"      :   director_id_and_name_dict["name"]
    })

def top_250_directors():
    directors_list = []

    for movie_item in MOVIE_ITEM_LIST:
        movie_detail_page = request_detail_page(movie_item)
        director_id_and_name_dict = director_finder(movie_detail_page)
        if check_director(directors_list, director_id_and_name_dict) == True:
            append_director(directors_list, director_id_and_name_dict)
            print(f"added to directors_list: {director_id_and_name_dict['name']}")
        else:
            print(f"already in directors_list: {director_id_and_name_dict['name']}")
            
    #we got everything what we want in directors_list
    with open("./jsons/directors.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(directors_list, indent=2))

top_250_directors()