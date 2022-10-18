from flask import(
    Blueprint,
    render_template,
    session,
    redirect,
    url_for
)

from imdb.main.general.utils import delete_watchlist
from .utils import (
    select_user_watchlist,
    users_movies_comments,
    users_actors_comments,
    select_users_informations,
    u_id,
    delete_watchlist,
    delete_movies_comemnts,
    delete_actors_comments,
    delete_users,
)


profile = Blueprint("profile", __name__, url_prefix="/profile")


@profile.route("/<string:username>")
def my_profile(username):
    return render_template("profile/my_profile.html")


@profile.route("/watchlist/<string:username>")
def profile_watchlist(username):
    watchlist = select_user_watchlist(username)
    return render_template("profile/profile_watchlist.html",
                            watchlist=watchlist)


@profile.route("/comments/<string:username>")
def profile_comments(username):
    movie_comments = users_movies_comments(username)
    actor_comments = users_actors_comments(username)

    return render_template("profile/profile_comments.html",
                            movie_comments=movie_comments,
                            actor_comments=actor_comments)



@profile.route("/settings/<string:username>")
def profile_settings(username):
    uname = session["username"]
    user = select_users_informations(username)
    

    return render_template("profile/profile_settings.html",
                            user=user,
                            uname=uname)


@profile.route("/delete_accaunt/<string:uname>")
def delete_accaunt(uname):
    try:
        if uname == session["username"]:
            user_id = u_id(uname)
            delete_watchlist(user_id)
            delete_movies_comemnts(uname)
            delete_actors_comments(uname)
            delete_users(user_id)
            session.clear()
            return render_template("general/index.html")
    except KeyError:
        return redirect("profile_settings", username=uname)



