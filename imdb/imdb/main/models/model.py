from dataclasses import dataclass


@dataclass
class Movie:
    id: int
    imdb_id: str
    title: str
    poster: str
    year: str
    rank: str
    rate: str
    description: str

    def __init__(self, id, imdb_id=None, title=None, poster=None, year=None, rank=None, rate=None, description=None):
        self.id = id
        self.imdb_id = imdb_id
        self.title = title
        self.poster = poster
        self.year = year
        self.rank = rank
        self.rate = rate
        self.description = description


@dataclass
class Genre:
    id: int
    genre_title: str

    def __init__(self, id, genre_title=None):
        self.id = id
        self.genre_title = genre_title


@dataclass
class Actor:
    id: int
    imdb_id: str
    name: str
    photo: str

    def __init__(self, id=None, imdb_id=None, name=None, photo=None):
        self.id = id
        self.imdb_id = imdb_id
        self.name = name
        self.photo = photo


@dataclass
class Director:
    id: int
    imdb_id: str
    name: str

    def __init__(self, id=None, imdb_id=None, name=None):
        self.id = id
        self.imdb_id = imdb_id
        self.name = name


@dataclass
class MovieAndDirector:
    id: int
    imdb_id: str
    title: str
    poster: str
    year: str
    rank: str
    rate: str
    description: str

    def __init__(self, id, imdb_id=None, title=None, poster=None, year=None, rank=None, rate=None, description=None, director=None):
        self.id = id
        self.imdb_id = imdb_id
        self.title = title
        self.poster = poster
        self.year = year
        self.rank = rank
        self.rate = rate
        self.description = description
        self.director = director

@dataclass
class Comments:
    id: int
    username: str
    comment: str
    date: str

    def __init__(self, id, username=None, comment=None, date=None):
        self.id = id
        self.username = username
        self.comment = comment
        self.date = date



@dataclass
class ViewWatchlist:
    title: str
    poster: str
    movie_id: str

    def __init__(self, title=None, poster=None, movie_id=None):
        self.title = title
        self.poster = poster
        self.movie_id = movie_id


@dataclass
class UserMovieComments:
    username: str
    comment: str
    date: str
    movie_title: str

    def __init__(self, username=None, comment=None, date=None, movie_title=None):
        self.username = username
        self.comment = comment
        self.date = date
        self.movie_title = movie_title


@dataclass
class UserActorComments:
    username: str
    comment: str
    date: str
    actor_name: str

    def __init__(self, username=None, comment=None, date=None, actor_name=None):
        self.username = username
        self.comment = comment
        self.date = date
        self.actor_name = actor_name


@dataclass
class User:
    id: int
    username: str
    email: str
    password: str
    verify: bool
    profile_picture: str

    def __init__(self, id,username=None, email=None, password=None, verify=None, profile_picture=None):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
        self.verify = verify
        self.profile_picture = profile_picture


@dataclass
class Activities:
    activity_type: str
    username: str
    movie_comment: str
    actor_comment: str
    date: str
    movie_title: str
    actor_name: str
    movie_poster: str
    actor_photo: str
    movie_id: int
    actor_id: int

    def __init__(self, activity_type=None, username=None, movie_comment=None, actor_comment=None, date=None, movie_title=None, actor_name=None, movie_poster=None, actor_photo=None, movie_id=None, actor_id=None):
        self.activity_type = activity_type
        self.username = username
        self.movie_comment = movie_comment
        self.actor_comment = actor_comment
        self.date = date
        self.movie_title = movie_title
        self.actor_name = actor_name
        self.movie_poster = movie_poster
        self.actor_photo = actor_photo
        self.movie_id = movie_id
        self.actor_id = actor_id