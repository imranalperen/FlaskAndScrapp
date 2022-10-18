from top250.utils import (
    MOVIE_ITEM_LIST,
    imdb_id_finder,
    request_detail_page,
    movie_stars_finder,
    star_actor_imdb_id,
    brackets_comma_cleaner,
    director_finder,
    genre_finder,
    json,
    top250_dir_path
)
from dbconn import c, conn

def movie_db_id_finder(movie_imdb_id):
    sql = f"""
        SELECT id
        FROM movies
        WHERE imdb_id = '{movie_imdb_id}'
        """
    c.execute(sql)
    db_id = c.fetchone()  #(250,)
    brackets_comma_cleaner(db_id)
    return db_id


#---------------MOVIE ACTORS TABLE---------------#(M2M)

def actor_db_id_finder(star_imdb_id):
    sql = f"""
        SELECT id
        FROM actors
        WHERE imdb_id = '{star_imdb_id}'
        """
    c.execute(sql)
    db_id = c.fetchone()
    return db_id

def append_movie_actor(movie_actors_list, movie_db_id, actor_db_id):
    movie_actors_list.append({
        "movie_id"  :   movie_db_id,
        "actor_id"  :   actor_db_id
    })

def movie_actors():
    i = 0
    movie_actors_list = []
    for movie in MOVIE_ITEM_LIST:
        movie_imdb_id = imdb_id_finder(movie)           #tt0111161
        movie_db_id = movie_db_id_finder(movie_imdb_id) #primary key 1,3,4,...,250
        movie_db_id = brackets_comma_cleaner(movie_db_id)
        movie_detail_page = request_detail_page(movie)
        movie_stars = movie_stars_finder(movie_detail_page)
        for star in movie_stars:
            star_imdb_id = star_actor_imdb_id(star)
            actor_db_id = actor_db_id_finder(star_imdb_id)
            actor_db_id = brackets_comma_cleaner(actor_db_id)
            print(f"movie actors: {i}")
            i += 1
            append_movie_actor(movie_actors_list, movie_db_id, actor_db_id)
    
    with open(f"{top250_dir_path}\\jsons\\movie_actors.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(movie_actors_list, indent=2))


movie_actors()

#---------------MOVIE DIRECTORS TABLE---------------#(M2M)

def director_db_id_finder(director_imdb_id):
    sql = f"""
        SELECT id
        FROM directors
        WHERE imdb_id = '{director_imdb_id}'
        """
    c.execute(sql)
    db_id = c.fetchone()
    return db_id


def append_movie_director(movie_director_list, movie_db_id, director_db_id):
    movie_director_list.append({
        "movie_id" :   str(movie_db_id),
        "director_id"  :   str(director_db_id)
    })


def movie_directors():
    i = 0
    movie_director_list = []
    for movie in MOVIE_ITEM_LIST:
        #find movie and directors db ids
        #go detail page find director imdb_id
        #write this datas in a json
        movie_imdb_id = imdb_id_finder(movie)
        movie_db_id = movie_db_id_finder(movie_imdb_id)
        movie_db_id = brackets_comma_cleaner(movie_db_id)
        movie_detail_page = request_detail_page(movie)
        director_imdb_id = director_finder(movie_detail_page)
        director_db_id = director_db_id_finder(director_imdb_id)
        director_db_id = brackets_comma_cleaner(director_db_id)
        print(f"movie_direcotrs: {i}")
        i += 1
        append_movie_director(movie_director_list, movie_db_id, director_db_id)
    
    with open(f"{top250_dir_path}\\jsons\\movie_directors.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(movie_director_list, indent=2))

movie_directors()

#---------------MOVIE GENRE TABLE---------------#(O2M)

def genre_db_id_finder(genre):
    sql = f"""
        SELECT id
        FROM genres
        WHERE genre_title = '{genre}'
        """
    c.execute(sql)
    db_id = c.fetchone()
    return db_id

def append_movie_genre(movie_genres_list, movie_db_id, genre_db_id):
    movie_genres_list.append({
        "movie_id"   :   movie_db_id,
        "genre_id"         :   genre_db_id
    })

def movie_genres():
    i = 0
    movie_genres_list = []
    for movie in MOVIE_ITEM_LIST:
        movie_all_genres = []
        movie_imdb_id = imdb_id_finder(movie)
        movie_db_id = movie_db_id_finder(movie_imdb_id)
        movie_db_id = brackets_comma_cleaner(movie_db_id)
        movie_detail_page = request_detail_page(movie)
        movie_all_genres = genre_finder(movie_detail_page)
        for genre in movie_all_genres:
            genre = genre.find("span").text
            genre_db_id = genre_db_id_finder(genre)
            genre_db_id = brackets_comma_cleaner(genre_db_id)
            append_movie_genre(movie_genres_list, movie_db_id, genre_db_id)
            print(f"movie genres: {i}")
            i += 1
    
    with open(f"{top250_dir_path}\\jsons\\movie_genres.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(movie_genres_list, indent=2))

movie_genres()