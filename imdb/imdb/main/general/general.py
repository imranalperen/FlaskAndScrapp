import string
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    session,
    request,
)
from .utils import(
    select_actors_comments,
    select_movies,
    select_genres,
    select_movie_by_imdb_id,
    select_movies_by_genre,
    select_movie_stars,
    is_it_voice_actor,
    append_watchlist,
    delete_watchlist,
    select_watchlist_ids,
    select_actors_with_letter,
    select_actor_by_id,
    select_actor_movies,
    select_director,
    select_movies_comments,
    insert_movies_comments,
    insert_actors_comments,
    is_it_in_watchlist,
    count_of_comment_pages,
    movies_pager,
    activity_feed,
    searchbox_movies,
    searchbox_actors
)


general = Blueprint("general", __name__)


@general.route("/")
def index():
    return render_template("general/index.html")


@general.route("/movies")
def movies():
    #250 movies 25 movies per page
    total_pages = movies_pager()
    current_page = request.args.get("page", None)
    movies_list = select_movies(current_page)
    genres = select_genres()
    title = "All"

    #if logged ther is session["username"]
    try:
        username = session["username"]
        watchlist_movie_ids = select_watchlist_ids(username)
    except KeyError:
        watchlist_movie_ids = None

    return render_template("general/movies.html",
                            movies_list=movies_list,
                            genres=genres,
                            title=title,
                            watchlist_movie_ids=watchlist_movie_ids,
                            total_pages=total_pages)


@general.route("/add_watchlist/<string:movie_id>")
def add_watchlist(movie_id):
    #add and remove watchlkist there is no trciky stuff only regex
    username = session["username"]
    append_watchlist(username, movie_id)
    referer = request.headers.get("Referer")
    #http://127.0.0.1:5000/movies?page=1---->movies
    #http://127.0.0.1:5000/details/65----->Details
    #http://127.0.0.1:5000/movies/Adventure ---->Genre
    referer = referer.split("5000/")    #deploy ederken değiştirilmesi gerekli
    referer = referer[1]
    referer = referer.split("?")
    flag = 0

    try:
        page = referer[1]
        page = page.split("=")
        current_page = page[1]
        flag = 1
    except IndexError:
        referer = referer[0]
        referer = referer.split("/")

    #feeding activity
    activity_feed(movie_id, None, None)
    #############

    if flag == 1:
        return redirect(url_for("general.movies", page=current_page))
    elif referer[0] == "movies":
        #/movies/Adventure, /Action....
        return redirect(url_for("general.movies_by_genre", genre = referer[1]))
    elif referer[0] == "details":
        return redirect(url_for("general.details", movie_id=referer[1]))


@general.route("/remove_watchlist/<string:movie_id>")
def remove_watchlist(movie_id):
    username = session["username"]
    delete_watchlist(username, movie_id)
    referer = request.headers.get("Referer")
    referer = referer.split("5000/")    #deploy ederken değiştirlmesi gerekli
    referer = referer[1]
    referer = referer.split("?")
    flag = 0
    
    try:
        page = referer[1]
        page = page.split("=")
        current_page = page[1]
        flag = 1
    except IndexError:
        referer = referer[0]
        referer = referer.split("/")

    if flag == 1:
        return redirect(url_for("general.movies", page=current_page))
    elif referer[0] == "movies":
        #/movies/Adventure, /Action....
        return redirect(url_for("general.movies_by_genre", genre = referer[1]))
    elif referer[0] == "profile":
        return redirect(url_for("profile.profile_watchlist", username=username))
    elif referer[0] == "details":
        return redirect(url_for("general.details", movie_id=referer[1]))


@general.route("/movies/<string:genre>")
def movies_by_genre(genre):
    movies_list = select_movies_by_genre(genre)
    genres = select_genres()
    try:
        username = session["username"]
        watchlist_movie_ids = select_watchlist_ids(username)
    except KeyError:
        watchlist_movie_ids = None

    return render_template("general/movies.html",
                            movies_list=movies_list,
                            genres=genres,
                            title=genre,
                            watchlist_movie_ids=watchlist_movie_ids)


@general.route("/details/<string:movie_id>")
def details(movie_id):

    movie_details = select_movie_by_imdb_id(movie_id)
    actors = select_movie_stars(movie_id)
    voice_actor = is_it_voice_actor(movie_id)
    directors = select_director(movie_id)

    #find total number of comments
    #put 5 comments per page
    #find total page
    comment_page = request.args.get("page", None)
    comments = select_movies_comments(movie_id, comment_page)
    total_pages = count_of_comment_pages(movie_id, None)

    try:
        username = session["username"]
        flag = is_it_in_watchlist(username, movie_id)
    except KeyError:
        username = None
        flag = None


    return render_template("general/details.html",
                            movie_details=movie_details,
                            actors=actors,
                            voice_actor=voice_actor,
                            directors=directors,
                            comments=comments,
                            flag=flag,
                            total_pages=total_pages,
                            movie_id=movie_id,
                            username=username)


@general.route("/add_comment_movie/<string:movie_id>", methods=["POST"])
def add_comment_movie(movie_id):
    comment = request.form.get("comment_body")

    if len(comment) > 255:
        return redirect(url_for("general.details", movie_id=movie_id))

    insert_movies_comments(comment, movie_id)
    
    #feeding activity
    activity_feed(movie_id, None, comment)
    #############

    return redirect(url_for("general.details", movie_id=movie_id))


@general.route("/actors")
def actors():
    alphabet = list(string.ascii_uppercase)
    current_letter = request.args.get("letter", None)
    if current_letter == None:
        current_letter = "A"
    all_actors = select_actors_with_letter(current_letter)
    
    return render_template("general/actors.html",
                            all_actors=all_actors,
                            alphabet=alphabet)


@general.route("/actor_details/<string:actor_id>")
def actor_details(actor_id):
    actor = select_actor_by_id(actor_id)
    actor_movies = select_actor_movies(actor_id)

    comment_page = request.args.get("page", None)
    comments = select_actors_comments(actor_id, comment_page)
    total_pages = count_of_comment_pages(None, actor_id)

    return render_template("general/actor_details.html",
                            actor=actor,
                            actor_movies=actor_movies,
                            comments=comments,
                            total_pages=total_pages,
                            actor_id=actor_id)


@general.route("/add_comment_actors/<string:actor_id>", methods=["POST"])
def add_comment_actor(actor_id):
    comment = request.form.get("comment_body")

    if len(comment) > 255:
        return redirect(url_for("general.actor_details", actor_id=actor_id))
    
    insert_actors_comments(comment, actor_id)

    #feeding activity
    activity_feed(None, actor_id, comment)
    #############

    return redirect(url_for("general.actor_details", actor_id=actor_id))


@general.route("/search", methods=["POST", "GET"])
def search():
    searching_string = request.form.get("search_box_input").lower()
    movies = searchbox_movies(searching_string)
    actors = searchbox_actors(searching_string)
    lenmovies=len(movies)
    lenactors = len(actors)
    
    return render_template("general/results.html",
                            movies=movies,
                            actors=actors,
                            lenmovies=lenmovies,
                            lenactors=lenactors)

