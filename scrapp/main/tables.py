from dbconn import c, conn

def create_genres_table():
    SQL = """
        CREATE TABLE IF NOT EXISTS genres(
            id SERIAL PRIMARY KEY,
            genre_title VARCHAR(20)
        )
        """
    c.execute(SQL)
    conn.commit()


def create_movies_table():
    SQL = """
        CREATE TABLE IF NOT EXISTS movies(
            id SERIAL PRIMARY KEY,
            imdb_id TEXT,
            title TEXT,
            poster TEXT,
            year VARCHAR(10),
            rank VARCHAR(10),
            rate VARCHAR(10),
            description TEXT
        )
        """
    c.execute(SQL)
    conn.commit()


def create_directors_table():
    SQL = """
        CREATE TABLE IF NOT EXISTS directors(
            id SERIAL PRIMARY KEY,
            imdb_id TEXT,
            name TEXT
        )
        """
    c.execute(SQL)
    conn.commit()


def create_actors_table():
    SQL = """
        CREATE TABLE IF NOT EXISTS actors(
            id SERIAL PRIMARY KEY,
            imdb_id TEXT,
            name TEXT,
            photo TEXT
        )
        """
    c.execute(SQL)
    conn.commit()


def create_movies_actors_table():
    SQL = """
        CREATE TABLE IF NOT EXISTS movies_actors(
            id SERIAL PRIMARY KEY,
            actor_id INTEGER,
            movie_id INTEGER,
            
            FOREIGN KEY (movie_id)
                REFERENCES movies(id),
            FOREIGN KEY (actor_id)
                REFERENCES actors(id)
        )
        """
    c.execute(SQL)
    conn.commit()


def create_movies_directors_table():
    SQL = """
        CREATE TABLE IF NOT EXISTS movies_directors(
            id SERIAL PRIMARY KEY,
            movie_id INTEGER,
            director_id INTEGER,

            FOREIGN KEY (movie_id)
                REFERENCES movies(id),
            FOREIGN KEY (director_id)
                REFERENCES directors(id)
        )
        """
    c.execute(SQL)
    conn.commit()


def create_movies_genres_table():
    SQL = """
        CREATE TABLE IF NOT EXISTS movies_genres(
            id SERIAL PRIMARY KEY,
            movie_id INTEGER,
            genre_id INTEGER,

            FOREIGN KEY (movie_id)
                REFERENCES movies(id),
            FOREIGN KEY (genre_id)
                REFERENCES genres(id)
        )
        """
    c.execute(SQL)
    conn.commit()


def create_users_table():
    SQL = """
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username VARCHAR(30) UNIQUE,
            email VARCHAR (40) UNIQUE,
            password TEXT,
            verify BOOLEAN DEFAULT FALSE,
            profile_picture BYTEA
        )
        """
    c.execute(SQL)
    conn.commit()


def create_users_watchlist_table():
    SQL = """
        CREATE TABLE IF NOT EXISTS users_watchlist (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            movie_id INTEGER,

            FOREIGN KEY (user_id)
                REFERENCES users(id),
            FOREIGN KEY (movie_id)
                REFERENCES movies(id)
        )
        """
    c.execute(SQL)
    conn.commit()


def create_movies_comments_table():
    SQL = """
        CREATE TABLE IF NOT EXISTS movies_comments (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            movie_id INTEGER,
            comment VARCHAR(255),
            date DATE NOT NULL DEFAULT CURRENT_DATE,

            FOREIGN KEY (user_id)
                REFERENCES users(id),
            FOREIGN KEY (movie_id)
                REFERENCES movies(id)
        )
        """
    c.execute(SQL)
    conn.commit()


def create_actors_comments_table():
    SQL = """
        CREATE TABLE IF NOT EXISTS actors_comments (
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            actor_id INTEGER,
            comment VARCHAR(255),
            date DATE NOT NULL DEFAULT CURRENT_DATE,

            FOREIGN KEY (user_id)
                REFERENCES users(id),
            FOREIGN KEY (actor_id)
                REFERENCES actors(id)
        )
        """
    c.execute(SQL)
    conn.commit()


def create_activity_types():
    SQL = """
        CREATE TABLE IF NOT EXISTS activity_types(
            id SERIAL PRIMARY KEY,
            name VARCHAR(20)
        )
        """
    c.execute(SQL)
    conn.commit()

    sql = "INSERT INTO activity_types (name) VALUES ('ADD_WATCHLIST')"
    c.execute(sql)
    conn.commit()

    sql = "INSERT INTO activity_types (name) VALUES ('ADD_MOVIE_COMMENT')"
    c.execute(sql)
    conn.commit()

    sql = "INSERT INTO activity_types (name) VALUES ('ADD_ACTOR_COMMENT')"
    c.execute(sql)
    conn.commit()


def create_activities_table():
    SQL = """
        CREATE TABLE IF NOT EXISTS activities (
            id SERIAL PRIMARY KEY,
            activity_type_id INTEGER,
            user_id INTEGER,
            object_id INTEGER,
            date DATE NOT NULL DEFAULT CURRENT_DATE,
            date_for_sort TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (activity_type_id)
                REFERENCES activity_types(id),
            FOREIGN KEY (user_id)
                REFERENCES users(id)
        )
        """
    c.execute(SQL)
    conn.commit()



create_genres_table()
create_movies_table()
create_directors_table()
create_actors_table()
create_movies_actors_table()
create_movies_directors_table()
create_movies_genres_table()
create_users_table()
create_users_watchlist_table()
create_movies_comments_table()
create_actors_comments_table()
create_activity_types()
create_activities_table()