from dbconn import c, conn
from top250.utils import top250_dir_path
import json
import re


def insert_genres():
    with open(f"{top250_dir_path}\\jsons\\genres.json", "r", encoding="utf-8") as file:
        temp = file.read()
        genres = json.loads(temp)
    
    for genre in genres:
        category = genre["genre"]
        c.execute("INSERT INTO genres (genre_title) VALUES(%s)", (f"{category}",))
    conn.commit()


def insert_movies():
    with open(f"{top250_dir_path}\\jsons\\movies.json", "r", encoding="utf-8") as file:
        temp = file.read()
        movies = json.loads(temp)
    
    for movie in movies:
        imdb_id =   movie["imdb_id"]
        title   =   movie["title"]
        poster  =   movie["poster"]
        temp_year=   movie["year"]   #(2019)
        year    =   re.sub(r'[()]', '', temp_year)  #2019
        rank    =   movie["rank"]
        rate    =   movie["rate"]
        description = movie["description"]
        c.execute("""
            INSERT INTO movies (
                imdb_id,
                title,
                poster,
                year,
                rank,
                rate,
                description
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,(   f"{imdb_id}",
                    f"{title}",
                    f"{poster}",
                    f"{year}",
                    f"{rank}",
                    f"{rate}",
                    f"{description}",   )
                )
    conn.commit()


def insert_directors():
    with open(f"{top250_dir_path}\\jsons\\directors.json", "r", encoding="utf-8") as file:
        temp = file.read()
        directors = json.loads(temp)
    
    for director in directors:
        imdb_id =   director["imdb_id"] #/name/nm0001104/
        name    =   director["name"]
        c.execute("""
            INSERT INTO directors (
                imdb_id,
                name
            )
            VALUES (%s, %s)
            """,(   f"{imdb_id}",
                    f"{name}",  )
                )
    conn.commit()


def insert_actors():
    with open(f"{top250_dir_path}\\jsons\\actors.json", "r", encoding="utf-8") as file:
        temp = file.read()
        actors = json.loads(temp)

    for actor in actors:
        imdb_id =   actor["imdb_id"]    #/name/nm0000209/
        name    =   actor["name"]
        photo   =   actor["photo"]
        c.execute("""
            INSERT INTO actors (
                imdb_id,
                name,
                photo
            )
            VALUES (%s, %s, %s)
            """,(   f"{imdb_id}",
                    f"{name}",
                    f"{photo}", )
                )
    conn.commit()


insert_genres()
insert_movies()
insert_actors()
insert_directors()
