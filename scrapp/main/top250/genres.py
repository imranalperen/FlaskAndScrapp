from utils import (
    soup,
    json,
)


def imdb_genres():
    genres = []
    genres_list = soup.find("ul", {"class": "quicklinks"}).find_all("li", {"class": "subnav_item_main"})
    for genre in genres_list:
        genre_title = genre.find("a").text.strip()
        genres.append({
            "genre"     :   genre_title
        })

    with open("./jsons/genres.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(genres, indent=2))


    return genres


imdb_genres()