from top250.utils import top250_dir_path
import json
from dbconn import c, conn

def insert_movies_actors():
    with open (f"{top250_dir_path}\\jsons\\movie_actors.json", "r") as file:
        temp = file.read()
        movie_actors = json.loads(temp)

    for i in movie_actors:
        movie_id    =   i["movie_id"]
        actor_id    =   i["actor_id"]
        c.execute("""
            INSERT INTO movies_actors (
                movie_id,
                actor_id
            )
            VALUES (%s, %s)
            """,(   f"{movie_id}",
                    f"{actor_id}"   )
                )
    conn.commit()


def insert_movies_directors():
    with open(f"{top250_dir_path}\\jsons\\movie_directors.json", "r", encoding="utf-8") as file:
        temp = file.read()
        movie_directors = json.loads(temp)

    for i in movie_directors:
        movie_id =    i["movie_id"]
        director_id = i["director_id"]
        c.execute("""
            INSERT INTO movies_directors (
                movie_id,
                director_id
            )
            VALUES (%s, %s)
            """,(   f"{movie_id}",
                    f"{director_id}"   )
                )
    conn.commit()


def insert_movies_genres():
    with open(f"{top250_dir_path}\\jsons\\movie_genres.json", "r", encoding="utf-8") as file:
        temp = file.read()
        movie_genres = json.loads(temp)

    for i in movie_genres:
        movie_id    =   i["movie_id"]
        genre_id    =   i["genre_id"]
        c.execute("""
            INSERT INTO movies_genres (
                movie_id,
                genre_id
            )
            VALUES (%s, %s)
            """,(   f"{movie_id}",
                    f"{genre_id}"   )
                )
    conn.commit()


insert_movies_actors()
insert_movies_directors()
insert_movies_genres()