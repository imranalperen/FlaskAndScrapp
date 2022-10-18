from imdb.dbconn import c, conn
from imdb.main.models.model import (
    Activities
)

def all_activities():
    #activities.activity_type_id = 3 cuz of activity_types table id=3 ==> add_actor_comment
    sql = """
        SELECT
            activity_types.name AS activity_type,
            users.username,
            movies_comments.comment AS movie_comment,
            actors_comments.comment AS actor_comment,
            activities.date date,
            movies.title AS movie_title,
            actors.name AS actor_name,
            movies.poster,
            actors.photo,
            movies.id,
            actors.id,
            activities.date_for_sort as sort
        FROM activities
        INNER JOIN users ON users.id = activities.user_id
        INNER JOIN activity_types ON activity_types.id = activities.activity_type_id
        LEFT OUTER JOIN users_watchlist ON (users_watchlist.id = activities.object_id AND activities.activity_type_id = 1)
        LEFT OUTER JOIN movies_comments ON (movies_comments.id = activities.object_id AND activities.activity_type_id = 2)
        LEFT OUTER JOIN actors_comments ON (actors_comments.id = activities.object_id AND activities.activity_type_id = 3)
        LEFT OUTER JOIN movies ON (movies.id = users_watchlist.movie_id OR movies.id = movies_comments.movie_id)
        LEFT OUTER JOIN actors ON actors.id = actors_comments.actor_id
        ORDER BY
            sort DESC
        LIMIT 20
        """
    c.execute(sql)
    rows = c.fetchall()

    activities = []
    for row in rows:
        activities.append(
            Activities(
                activity_type=row[0],
                username=row[1],
                movie_comment=row[2],
                actor_comment=row[3],
                date=row[4],
                movie_title=row[5],
                actor_name=row[6],
                movie_poster=row[7],
                actor_photo=row[8],
                movie_id=row[9],
                actor_id=row[10]
            )
        )

    return activities
