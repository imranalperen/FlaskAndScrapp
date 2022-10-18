from imp import C_EXTENSION
from imdb.dbconn import c, conn
from imdb.main.models.model import (
    UserActorComments,
    UserMovieComments,
    User,
    ViewWatchlist,
)


def select_user_watchlist(username):
    #users.username to movies.title...
    sql = f"""
        SELECT movies.title, movies.poster, movies.id
        FROM movies
        INNER JOIN users_watchlist ON users_watchlist.movie_id = movies.id
        INNER JOIN users ON users.id = users_watchlist.user_id
        WHERE users.username = '{username}'
        """
    c.execute(sql)
    rows = c.fetchall()
    
    watchlist = []
    for row in rows:
        watchlist.append(
            ViewWatchlist(
                title=row[0],
                poster=row[1],
                movie_id=row[2]
            )
        )
        
    return watchlist


def users_movies_comments(username):
    sql = f"""
        SELECT users.username, movies_comments.comment, movies_comments.date, movies.title
        FROM movies_comments
        INNER JOIN users ON users.id = movies_comments.user_id
        INNER JOIN movies ON movies.id = movies_comments.movie_id
        WHERE users.username = '{username}'
        """
    c.execute(sql)
    rows = c.fetchall()

    comments = []
    for row in rows:
        comments.append(
            UserMovieComments(
                username=row[0],
                comment=row[1],
                date=row[2],
                movie_title=row[3]
            )
        )
    
    return comments

    

def users_actors_comments(username):
    sql = f"""
        SELECT users.username, actors_comments.comment, actors_comments.date, actors.name
        FROM actors_comments
        INNER JOIN users ON users.id = actors_comments.user_id
        INNER JOIN actors ON actors.id = actors_comments.actor_id
        WHERE users.username = '{username}'
        """
    c.execute(sql)
    rows = c.fetchall()

    comments = []
    for row in rows:
        comments.append(
                UserActorComments(
                username=row[0],
                comment=row[1],
                date=row[2],
                actor_name=row[3]
            )
        )
    
    return comments


def select_users_informations(username):
    sql = f"""
        SELECT id, username, email, password, verify, profile_picture
        FROM users
        WHERE username = '{username}'
        """
    c.execute(sql)
    rows = c.fetchall()
    
    user = []
    for row in rows:
        user.append(
            User(
                id=row[0],
                username=row[1],
                email=row[2],
                password=row[3],
                verify=row[4],
                profile_picture=row[5]
            )
        )

    return user


def u_id(username):
    sql = f"SELECT id FROM users WHERE username = '{username}'"
    c.execute(sql)
    row = c.fetchone()
    user_id = row[0]

    return user_id

def delete_watchlist(user_id):
    try:
        sql = f"DELETE FROM users_watchlist WHERE user_id = '{user_id}'"
        c.execute(sql)
        conn.commit()
    except TypeError:
        pass


def delete_movies_comemnts(username):
    try:
        sql = f"DELETE FROM movies_comments WHERE username = '{username}'"
        c.execute(sql)
        conn.commit()
    except TypeError:
        pass


def delete_actors_comments(username):
    try:
        sql = f"DELETE FROM actors_comments WHERE username = '{username}'"
        c.execute(sql)
        conn.commit()
    except TypeError:
        pass


def delete_users(user_id):
    try:
        sql = f"DELETE FROM users WHERE id = '{user_id}'"
        c.execute(sql)
        conn.commit()
    except TypeError:
        pass




