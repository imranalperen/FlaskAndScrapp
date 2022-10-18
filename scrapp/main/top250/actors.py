from .utils import (
    json,
    re,
    requests,
    request_detail_page,
    BeautifulSoup,
    BASE_URL,
    MOVIE_ITEM_LIST,
    movie_stars_finder,
)


def star_actor_id_and_name(star):
    star_actor = {}
    temp = star.find("a")["href"]
    temp = re.split("\?", temp)
    star_actor["imdb_id"] = temp[0] #/name/nm0000209/
    star_actor["name"] = star.find("a").text
    return star_actor

def check_star(actors_list, id_name_dict):
    if len(actors_list) == 0:
        return True
    else:
        for i in range(len(actors_list)):
            if id_name_dict["imdb_id"] == actors_list[i]["imdb_id"]:
                return False
            
        return True

def actor_photo_finder(id):
    detail = requests.get(BASE_URL + id)
    detail_soup = BeautifulSoup(detail.content, "html.parser")
    try:
        photo = detail_soup.find("body")
        photo = photo.find("div", {"id": "wrapper"})
        photo = photo.find("div", {"class": "pagecontent"})
        photo = photo.find("div", {"class": "redesign"})
        photo = photo.find("div", {"class": "maindetails_center"})
        photo = photo.find("div", {"class": "article name-overview with-hero"})
        photo = photo.find("div", {"class": "name-overview-widget"})
        photo = photo.find("table", {"id": "name-overview-widget-layout"})
        photo = photo.find("tbody")
        photo = photo.find_all("tr")[1]
        photo = photo.find("td", {"id": "img_primary"})
        photo = photo.find("div", {"class": "poster-hero-container"})
        photo = photo.find("div", {"class": "image"})
        photo = photo.find("a")
        photo = photo.find("img")["src"]
        return photo
    except:
        #anonym profile photo
        photo = "https://m.media-amazon.com/images/S/sash/9FayPGLPcrscMjU.png"
        return photo

def append_actor(actors_list, id_name_dict):
    photo = actor_photo_finder(id_name_dict["imdb_id"])
    actors_list.append({
        "imdb_id"   :   id_name_dict["imdb_id"],
        "name"      :   id_name_dict["name"],
        "photo"     :   photo
    })

def imdb_top_250_movies_actors():
    actors_list = []

    for movie_item in MOVIE_ITEM_LIST:
        movie_detail_page = request_detail_page(movie_item)
        movie_stars = movie_stars_finder(movie_detail_page)
        for star in movie_stars:
            id_name_dict = star_actor_id_and_name(star)
            if check_star(actors_list, id_name_dict) == True:
                append_actor(actors_list, id_name_dict)
                print(f"added: {id_name_dict['name']}")
            else:
                print(f"already in actors: {id_name_dict['name']}")
                
        #we got everything what we want in actors_list
        with open("./jsons/actors.json", "w", encoding="utf-8") as file:
            file.write(json.dumps(actors_list, indent=2))
    return actors_list


imdb_top_250_movies_actors()