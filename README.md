![image](https://user-images.githubusercontent.com/33910768/196524667-5b9d76e3-68ef-467e-99d3-a90902cd30cf.png)

This is a movie and actor review platform using imdb top 250 datas. I used BeautifulSoup for scraping imdb datas and Flask, Python, PostgreSQL for webapp. Also this is my first project of learning backend development.

### Requirements FlaskMovies

| Package | Version |
| ----------- | ----------- |
| colorama | 0.4.5 |
| Flask | 2.2.2 |
| itsdangerous | 2.1.2 |
| Jinja2 | 3.1.2 |
| MarkupSafe | 2.1.1 |
| pip | 22.2.2 |
| psycopg2 | 2.9.4 |
| setuptools | 63.2. |
| Werkzeug | 2.2. |

## Requirements Scrapp

| Package | Version |
| ----------- | ----------- |
| beautifulsoup4 | 4.11.1 |
| bs4 | 0.0.1 |
| certifi | 2022.9.24 |
| charset | normalizer 2.1.1 |
| idna | 3.4 |
| pip | 22.3 |
| psycopg2 | 2.9.4 |
| requests | 2.28.1 |
| setuptools | 63.2.0 |
| soupsieve | 2.3.2.post1 |
| urllib3 | 1.26.12 |

### RUN FLASK MOVIES WEBAPP

1. your/path/wbapp/scrapp/main/dbconn.py set your db conn
2. your/path/wbapp/scrapp/main/tables.py	run
3. your/path/wbapp/scrapp/main/insertdb.py	run
4. your/path/wbapp/scrapp/main/insertdbm2m.py	run
5. your/path/wbapp/imdb/imdb/dbconn.py	set your db connection
6. your/path/wbapp/imdb>  go directory with cmd and run:
```
set FLASK_APP=imdb
flask run
```

*will run your local host, also you can run in debug, set app.py to run.py, select python flask instead of python*


### RUN SCRAPP
1. your/path/scrapp/main/top250/jsons	delete all .json files  
*step 2,3,4,5 you can run at same time from different cmd windows, it takes 15+ mins for me*  

2. your/path/wbapp/scrapp/main/top250/actors.py	run  
3. your/path/wbapp/scrapp/main/top250/directors.py	run  
4. your/path/wbapp/scrapp/main/top250/genres.py	run  
5. your/path/wbapp/scrapp/main/top250/movies.py	run  
*other steps one by one*  

6. your/path/wbapp/scrapp/main/m2m_scraping.py	run  
7. your/path/wbapp/scrapp/main/dbconn.py		set your db connection  
8. your/path/wbapp/scrapp/main/tables.py		run  
9. your/path/wbapp/scrapp/main/insertdb.py		run  
10. your/path/wbapp/scrapp/main/insertdbm2m.py	run  
