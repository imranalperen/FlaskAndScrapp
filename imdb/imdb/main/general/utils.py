from flask import session
import math
import imdb
from imdb.dbconn import c, conn
from imdb.main.models.model import (
    Movie,
    Genre,
    Actor,
    Director,
    MovieAndDirector,
    Comments
)


def select_movies(current_page):
    if current_page == None:
        offset = 0
    else:
        offset = (int(current_page)-1)*25
    sql = f"""
        SELECT id, imdb_id, title, poster, year, rank, rate, description
        FROM movies
        LIMIT 25
        OFFSET {offset}
        """
    c.execute(sql)
    rows = c.fetchall()
    movies = []
    for row in rows:
        movies.append(
            Movie(
                id=row[0],
                imdb_id=row[1],
                title=row[2],
                poster=row[3],
                year=row[4],
                rank=row[5],
                rate=row[6],
                description=row[7],
            )
        )
    return movies


def movies_pager():
    #250 movies 25 movies per page
    total_page = 10
    total_pages = []
    for i in range(int(total_page)):
        total_pages.append(str(i+1))

    return total_pages


def select_genres():
    sql = """
        SELECT id, genre_title FROM genres
        """
    c.execute(sql)
    rows = c.fetchall()
    genres = []
    for row in rows:
        genres.append(
            Genre(
                id=row[0],
                genre_title=row[1]
            )
        )
    return genres


def append_watchlist(username, movie_id):
    sql = f"SELECT users.id FROM users WHERE username = '{username}'"
    c.execute(sql)
    row = c.fetchone()
    user_id = row[0]

    sql = f"INSERT INTO users_watchlist (user_id, movie_id) VALUES ({user_id}, {movie_id})"
    c.execute(sql)
    conn.commit()


def delete_watchlist(username, movie_id):
    sql = f"SELECT users.id FROM users WHERE username = '{username}'"
    c.execute(sql)
    row = c.fetchone()
    user_id = row[0]


    sql = f"DELETE FROM users_watchlist WHERE user_id = '{user_id}' AND movie_id = '{movie_id}'"
    c.execute(sql)
    conn.commit()


def select_watchlist_ids(username):

    #username to users_watchlist.movie_id
    sql = f"""
        SELECT movie_id
        FROM users_watchlist
        INNER JOIN users ON users.id = users_watchlist.user_id
        WHERE users.username = '{username}'
        """
    c.execute(sql)
    rows = c.fetchall()

    watchlist = []
    for row in rows:
        watchlist.append(row[0])
    #returns movie_id(s)
    return watchlist


def select_movies_by_genre(genre):
    sql = f"""
        SELECT movies.id, imdb_id, title, poster, year, rank, rate, description
        FROM movies
        INNER JOIN movies_genres ON movies_genres.movie_id = movies.id
        INNER JOIN genres ON genres.id = movies_genres.genre_id
        WHERE genres.genre_title = '{genre}'
        """
    c.execute(sql)
    rows = c.fetchall()
    movies = []
    for row in rows:
        movies.append(
            Movie(
                id=row[0],
                imdb_id=row[1],
                title=row[2],
                poster=row[3],
                year=row[4],
                rank=row[5],
                rate=row[6],
                description=row[7],
            )
        )
    return movies


def select_movie_by_imdb_id(movie_id):
    sql = f"""
        SELECT id, imdb_id, title, poster, year, rank, rate, description
        FROM movies
        WHERE id = '{movie_id}'
        """
    c.execute(sql)
    rows = c.fetchall()
    movies = []
    for row in rows:
        movies.append(
            Movie(
                id=row[0],
                imdb_id=row[1],
                title=row[2],
                poster=row[3],
                year=row[4],
                rank=row[5],
                rate=row[6],
                description=row[7],
            )
        )
    return movies


def select_movie_stars(movie_id):
    sql = f"""
        SELECT actors.id, actors.imdb_id, name, photo
        FROM actors
        INNER JOIN movies_actors ON movies_actors.actor_id = actors.id
        INNER JOIN movies ON movies.id = movies_actors.movie_id
        WHERE movies.id = '{movie_id}'
        """
    c.execute(sql)
    rows = c.fetchall()
    actors = []
    for row in rows:
        actors.append(
            Actor(
                id=row[0],
                imdb_id=row[1],
                name=row[2],
                photo=row[3],
            )
        )
    return actors


def is_it_voice_actor(movie_id):
    #if there is an animation movie there is no stars
    #it should be vice actor
    sql = f"""
        SELECT genres.id, genre_title
        FROM genres
        INNER JOIN movies_genres ON movies_genres.genre_id = genres.id
        INNER JOIN movies ON movies.id = movies_genres.movie_id
        WHERE movies.id = '{movie_id}'
        """
    c.execute(sql)
    rows = c.fetchall()
    #[(3, 'Animation'), (2, 'Adventure'), (8, 'Family')]
    for row in rows:
        if row[1] == 'Animation':
            return True
    return False


def select_director(movie_id):
    sql = f"""
        SELECT directors.id, directors.imdb_id, name
        FROM directors
        INNER JOIN movies_directors ON movies_directors.director_id = directors.id
        INNER JOIN movies ON movies.id = movies_directors.movie_id
        WHERE movies.id = '{movie_id}'
        """
    c.execute(sql)
    rows = c.fetchall()
    director = []
    for row in rows:
        director.append(
            Director(
                id=row[0],
                imdb_id=row[1],
                name=row[2]
            )
        )
    return director


def select_actors_with_letter(letter):
    sql = f"SELECT id, imdb_id, name, photo FROM actors WHERE name LIKE '{letter}%'"
    c.execute(sql)
    rows = c.fetchall()
    actors = []
    for row in rows:
        actors.append(
            Actor(
                id=row[0],
                imdb_id=row[1],
                name=row[2],
                photo=row[3]
            )
        )
    return actors


def select_actor_by_id(actor_id):
    sql = f"SELECT id, imdb_id, name, photo FROM actors WHERE id = '{actor_id}'"
    c.execute(sql)
    rows = c.fetchall()
    actor = []
    for row in rows:
        actor.append(
            Actor(
                id=row[0],
                imdb_id=row[1],
                name=row[2],
                photo=row[3]
            )
        )
    return actor


def select_actor_movies(actor_id):
    sql = f"""
        SELECT movies.id, movies.imdb_id, title, poster, year, rank, rate, description, directors.name
        FROM movies
        INNER JOIN movies_actors ON movies_actors.movie_id = movies.id
        INNER JOIN actors ON actors.id = movies_actors.actor_id
        INNER JOIN movies_directors ON movies.id = movies_directors.movie_id
        INNER JOIN directors ON directors.id = movies_directors.director_id
        WHERE actors.id = '{actor_id}'
        """
    c.execute(sql)
    rows = c.fetchall()
    actor_movies = []
    for row in rows:
        actor_movies.append(
            MovieAndDirector(
                id=row[0],
                imdb_id=row[1],
                title=row[2],
                poster=row[3],
                year=row[4],
                rank=row[5],
                rate=row[6],
                description=row[7],
                director=row[8]
            )
        )
    return actor_movies


def insert_movies_comments(comment, movie_id):
    username = session["username"]
    sql = f"SELECT id FROM users WHERE username = '{username}'"
    c.execute(sql)
    row = c.fetchone()
    user_id = row[0]

    sql = f"""
        INSERT INTO movies_comments (user_id, movie_id, comment)
        VALUES ('{user_id}', '{movie_id}', '{comment}')
        """
    c.execute(sql)
    conn.commit()


def select_movies_comments(movie_id, comment_page):
    if comment_page == None:
        offset = 0
    else:
        offset = (int(comment_page)-1)*5


    sql = f"""
        SELECT movies_comments.id, users.username, movies_comments.comment, movies_comments.date
        FROM movies_comments
        INNER JOIN users ON users.id = movies_comments.user_id
        INNER JOIN movies ON movies.id = movies_comments.movie_id
        WHERE movies.id = '{movie_id}'
        LIMIT 5
        OFFSET {offset}
        """
    c.execute(sql)
    rows = c.fetchall()
    comments = []
    for row in rows:
        comments.append(
            Comments(
                id=row[0],
                username=row[1],
                comment=row[2],
                date=row[3]
            )
        )
    return comments


def round_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


def count_of_comment_pages(movie_id, actor_id):
    #using at actor details and movie details
    #where you use make other None
    if actor_id == None:
        sql = f"SELECT COUNT(id) FROM movies_comments WHERE movie_id = '{movie_id}'"
        c.execute(sql)
        row = c.fetchone()
        total_comments = row[0]
    else:
        sql = f"SELECT COUNT(id) FROM actors_comments WHERE actor_id = '{actor_id}'"
        c.execute(sql)
        row = c.fetchone()
        total_comments = row[0]

    if total_comments <= 5:
        pages = 1
    else:
        pages = round_up(total_comments/5)

    pages = int(pages)
    page_list = []
    for i in range(pages):
        page_list.append(str(i+1))

    return page_list


def insert_actors_comments(comment, actor_id):
    username = session["username"]

    sql = f"SELECT id FROM users WHERE username = '{username}'"
    c.execute(sql)
    row = c.fetchone()
    user_id = row[0]


    sql = f"""
        INSERT INTO actors_comments (user_id, actor_id, comment)
        VALUES ('{user_id}', '{actor_id}', '{comment}')
        """
    c.execute(sql)
    conn.commit()


def select_actors_comments(actor_id, comment_page):
    if comment_page == None:
        offset = 0
    else:
        offset = (int(comment_page)-1)*5

    sql = f"""
        SELECT actors_comments.id, users.username, actors_comments.comment, actors_comments.date
        FROM actors_comments
        INNER JOIN users ON users.id = actors_comments.user_id
        INNER JOIN actors ON actors.id = actors_comments.actor_id
        WHERE actors.id = '{actor_id}'
        LIMIT 5
        OFFSET {offset}
        """
    c.execute(sql)
    rows = c.fetchall()
    comments = []
    for row in rows:
        comments.append(
            Comments(
                id=row[0],
                username=row[1],
                comment=row[2],
                date=row[3]
            )
        )
    return comments


def is_it_in_watchlist(username, movie_id):
    #usname to user_id
    #movie_imdb_id to movie_id
    #query users_watchlist

    sql = f"SELECT id FROM users WHERE username = '{username}'"
    c.execute(sql)
    row = c.fetchall()
    user_id = row[0][0]

    sql = f"""
            SELECT id FROM users_watchlist
            WHERE
                movie_id = '{movie_id}' AND user_id = '{user_id}'
            """
    c.execute(sql)
    row = c.fetchall()

    if row == []:
        return False
    else:
        return True


def watchlist_last_row_id():
    sql = """
        SELECT id FROM users_watchlist
            ORDER BY
                id DESC
            LIMIT 1
        """
    c.execute(sql)
    row = c.fetchone()
    return row[0]





def activity_feed(movie_id, actor_id, comment):
    username = session["username"]
    sql = f"SELECT id FROM users WHERE username = '{username}'"
    c.execute(sql)
    row = c.fetchone()
    user_id = row[0]

    if movie_id == None:
        #actor comment
        activity_type_id = 3 #set as 3 cuz of activity_types table
        #reaching object_id
        sql = f"""
            SELECT id FROM actors_comments
            ORDER BY
                id DESC
            LIMIT 1
            """
        c.execute(sql)
        row = c.fetchone()
        object_id = row[0]
        #insert table
        sql = f"""
            INSERT INTO activities (activity_type_id, user_id, object_id)
            VALUES ('{activity_type_id}', '{user_id}', '{object_id}')
            """
        c.execute(sql)
        conn.commit()

    elif actor_id == None and comment == None:
        #add watchlist
        activity_type_id = 1
        sql = f"""
            SELECT id FROM users_watchlist
            ORDER BY 
                id DESC
            LIMIT 1
            """
        c.execute(sql)
        row = c.fetchone()
        object_id = row[0]

        sql = f"""
            INSERT INTO activities (activity_type_id, user_id, object_id)
            VALUES ('{activity_type_id}', '{user_id}', '{object_id}')
            """
        c.execute(sql)
        conn.commit()

    else:
        #movie comment
        activity_type_id = 2
        sql = f"""
            SELECT id FROM movies_comments
            ORDER BY
                id DESC
            LIMIT 1
            """
        c.execute(sql)
        row = c.fetchone()
        object_id = row[0]

        sql = f"""
            INSERT INTO activities (activity_type_id, user_id, object_id)
            VALUES ('{activity_type_id}', '{user_id}', '{object_id}')
            """
        c.execute(sql)
        conn.commit()


def searchbox_movies(string):
    sql = f"""
        SELECT id, imdb_id, title, poster, year, rank, rate, description
        FROM movies
        WHERE LOWER(title) LIKE '%{string}%'
        """
    c.execute(sql)
    rows = c.fetchall()
    if rows != None:
        movies = []
        for row in rows:
            movies.append(
                Movie(
                    id=row[0],
                    imdb_id=row[1],
                    title=row[2],
                    poster=row[3],
                    year=row[4],
                    rank=row[5],
                    rate=row[6],
                    description=row[7]
                )
            )
        return movies
    return None


def searchbox_actors(string):
    sql = f"""
        SELECT id, imdb_id, name, photo
        FROM actors
        WHERE LOWER(name) LIKE '%{string}%'
        """
    c.execute(sql)
    rows = c.fetchall()
    if rows != None:
        actors = []
        for row in rows:
            actors.append(
                Actor(
                    id=row[0],
                    imdb_id=row[1],
                    name=row[2],
                    photo=row[3]
                )
            )
        return actors
    return None



