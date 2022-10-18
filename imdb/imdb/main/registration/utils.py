from imdb.dbconn import c, conn
import hashlib
import re
from email.message import EmailMessage
import ssl
import smtplib
import random


def brackets_comma_cleaner(argument):
    argument = str(argument)
    argument = re.sub(r'[(,\')]', "", argument)
    return argument


def check_email_db(email):
    sql = f"""
        SELECT email FROM users
        WHERE email = '{email}'
        """
    c.execute(sql)
    dbmail = c.fetchall()
    if dbmail != []:
        return False
    elif len(email) > 40:
        return False
        
    return True


def check_username_db(username):
    sql = f"""
        SELECT username FROM users
        WHERE username = '{username}'
        """
    c.execute(sql)
    dbusername = c.fetchall()
    if dbusername != []:
        return False
    
    return True


def match_passwords(psw, verify_psw):
    if psw != verify_psw:
        return False

    return True


def hash_password(password, username):
    string = password + username
    string = hashlib.sha256(password.encode('utf-8')).hexdigest()
    return string


def add_user_db(email, username, hashed_password):
    sql = f"""
        INSERT INTO users (email, username, password)
        VALUES ('{email}', '{username}', '{hashed_password}')
        """
    c.execute(sql)
    conn.commit()


def check_password(username, hashed_password):
    sql = f"""
        SELECT password FROM users
        WHERE username = '{username}'
        """
    c.execute(sql)
    psw = c.fetchone()
    psw = brackets_comma_cleaner(psw)
    
    if psw == hashed_password:
        return True
    
    return False


def code_mail(mail_adress):
    email_sender = "pythonblogtest@gmail.com"
    email_password = "lkvziuktllpgxiep"
    email_receiver = mail_adress
    subject = "VERIFY MAIL"
    random_number = random.randint(1000,9999)
    body = f"Your verify code: {random_number}"
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["Subject"] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
    return random_number


def get_username(email):
    sql = f"""
        SELECT username FROM users
        WHERE email = '{email}'
        """
    c.execute(sql)
    uname = brackets_comma_cleaner(c.fetchone())
    return uname


def update_password(hashed_password, username):
    sql = f"""
        UPDATE users
        SET password = '{hashed_password}'
        WHERE username = '{username}'
        """
    c.execute(sql)
    conn.commit()


