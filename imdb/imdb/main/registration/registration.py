from flask import (
    Blueprint,
    render_template,
    request,
    url_for,
    redirect,
    session,
    )
from .utils import(
    check_email_db,
    check_username_db,
    hash_password,
    match_passwords,
    add_user_db,
    check_password,
    code_mail,
    get_username,
    update_password,
)


registeration = Blueprint("registration", __name__)



@registeration.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        error = ""
        email = request.form.get("email").lower()
        username = request.form.get("username").lower()
        password = request.form.get("password")
        verify_passowrd = request.form.get("verify_password")

        if check_email_db(email) != True:
            if len(email) > 40:
                error = "Email too long."
                return render_template("registration/signup.html", error=error)
            error = "This mail already registered."
            return render_template("registration/signup.html", error=error)
        if check_username_db(username) != True:
            if len(username) > 30:
                error = "Username too long."
                return render_template("registration/signup.html", error=error)
            error = "This username already using."
            return render_template("registration/signup.html", error=error)
        if match_passwords(password, verify_passowrd) != True:
            error = "Passwords must match."
            return render_template("registration/signup.html", error=error)
            
        hashed_password = hash_password(password, username)
        add_user_db(email, username, hashed_password)
        return redirect(url_for("registration.login"))

    return render_template("registration/signup.html")


@registeration.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username").lower()
        password = request.form.get("password")
        if check_username_db(username) == False: #there is a user that username
            hashed_psw = hash_password(password, username)
            if check_password(username, hashed_psw) == True:
                session["username"] = username
                return redirect(url_for("general.index"))
            
            error = "Invalid password"
            return render_template("registration/login.html", error=error)

        error = "Invalid username"
        return render_template("registration/login.html", error=error)

    return render_template("registration/login.html")


@registeration.route("/forgotpassword", methods=["GET", "POST"])
def forgotpassword():
    if request.method == "POST":
        email = request.form.get("email")
        flag = 1

        try:
            if check_email_db(email) == False:  #if mail in db
                code = code_mail(email)
                session["code"] = code
                #emil in session if not emil input ll be None
                session["email"] = email
                return render_template("registration/forgotpassword.html", flag=flag, email=email)

        except TypeError:
            #unpack email and send html for dodge None email input
            email = session["email"]
            user_code = str(request.form.get("code"))
            password = request.form.get("password")
            verify_password = request.form.get("verify_password")
            if password == verify_password:
                if user_code == str(session["code"]):
                    username = get_username(email)
                    hashed_psw = hash_password(password, username)
                    update_password(hashed_psw, username)
                    return redirect(url_for("registration.login"))

                error = "Invalid verify code."
                return render_template("registration/forgotpassword.html",
                                        flag=flag, email=email, error=error)

            error = "Passwords must match."
            return render_template("registration/forgotpassword.html",
                                    flag=flag, email=email, error=error)

        error = "Invalid email."
        return render_template("registration/forgotpassword.html",
                                flag=flag, email=email, error=error)

    return render_template("registration/forgotpassword.html")


@registeration.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("general.index"))


