DB_HOST = "localhost"
DB_NAME = "imdb"
DB_USER = "postgres"
DB_PASS = "qwe"
import psycopg2


conn = psycopg2.connect(dbname  =   DB_NAME,
                        user    =   DB_USER,
                        password=   DB_PASS,
                        host    =   DB_HOST)
c = conn.cursor()