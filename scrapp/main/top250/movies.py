from utils import (
    request_detail_page,
    re,
    json,
    MOVIE_ITEM_LIST,
    imdb_id_finder,
    requests,
    BeautifulSoup,
)


def title_finder(movie):
    title = movie.find("td", {"class": "titleColumn"}).find("a").text
    return title


def poster_finder(imdb_id):
    BASE_URL = "https://www.imdb.com/title/"
    r = requests.get(BASE_URL + imdb_id)
    soup = BeautifulSoup(r.content, "html.parser")
    try:
        poster = soup.find("div", {"class": "sc-2a827f80-2 kqTacj"})
        poster = poster.find("div", {"class": "sc-2a827f80-3 dhWlsy"})
        poster = poster.find("div", {"class": "sc-77a2c808-0 fbPzfF"})
        poster = poster.find("div", {"class": "sc-77a2c808-1 gFDKno"})
        poster = poster.find("div", {"class": "ipc-poster ipc-poster--baseAlt ipc-poster--dynamic-width sc-d383958-0 gvOdLN celwidget ipc-sub-grid-item ipc-sub-grid-item--span-2"})
        poster = poster.find("a", {"class": "ipc-lockup-overlay ipc-focusable"})["href"]
    except:
        poster = soup.find("div", {"class": "sc-2a827f80-6 jXSdID"})
        poster = poster.find("div", {"sc-2a827f80-7 cOVoYS"})
        poster = poster.find("div", {"class": "sc-77a2c808-6 ioHyQT"})
        poster = poster.find("div", {"class": "ipc-poster ipc-poster--baseAlt ipc-poster--dynamic-width sc-d383958-0 gvOdLN celwidget ipc-sub-grid-item ipc-sub-grid-item--span-2"})
        poster = poster.find("a", {"class": "ipc-lockup-overlay ipc-focusable"})["href"]
    poster = "https://www.imdb.com" + poster
    ch = "?"
    poster = poster.split(ch, 1)[0]

    r = requests.get(poster)
    soup = BeautifulSoup(r.content, "html.parser")
    try:
        poster = soup.find("div", {"class": "ipc-page-content-container ipc-page-content-container--full sc-10d45a83-0 kelRIf"})
        poster = poster.find("div", {"class": "sc-92eff7c6-1 gHPZBs media-viewer"})
        poster = poster.find("div", {"class": "sc-7c0a9e7c-2 bkptFa"})
        poster = poster.find("img")["src"]

    except:
        poster = soup.find("div", {"class": "ipc-page-content-container ipc-page-content-container--full sc-10d45a83-0 kelRIf"})
        poster = poster.find("div", {"class": "sc-92eff7c6-1 gHPZBs media-viewer"})
        poster = poster.find("div", {"class": "sc-7c0a9e7c-3 dVABsL"})
        poster = poster.find("img")["src"]
    
    return poster


def year_finder(movie):
    year = movie.find("td", {"class": "titleColumn"}).find("span", {"class": "secondaryInfo"}).text.strip()
    return year


def rank_finder(movie):
    rank = movie.find("td", {"class" : "titleColumn"}).text.strip()
    rank = re.split("\.", rank)
    rank = rank[0]
    return rank


def rate_finder(movie):
    rate = movie.find("td", {"class": "ratingColumn imdbRating"}).find("strong").text
    return rate


def description_finder(movie):
    detail_soup = request_detail_page(movie)
    try:
        temp = detail_soup.find("div", {"class": "sc-16ede01-8 hXeKyz sc-2a827f80-11 kSXeJ"})
        temp = temp.find("p", {"class": "sc-16ede01-6 cXGXRR"})
        #if long there is a long description there is a read more 
        try:
            description = temp.find("span", {"class": "sc-16ede01-1 kgphFu"}).text
        except:
            description = temp.find("span", {"class": "sc-16ede01-0 fMPjMP"}).text
    except: #detail pages which dont have teaser video
        temp = detail_soup.find("div", {"class":"sc-16ede01-7 hrgVKw"})
        description = temp.find("span", {"class": "sc-16ede01-0 fMPjMP"}).text
    return description


def append_movies(movies_list, imdb_id, title, poster, year, rank, rate, description):
        movies_list.append({
        "imdb_id"   :   imdb_id,
        "title"     :   title,
        "poster"    :   poster,
        "year"      :   year,
        "rank"      :   rank,
        "rate"      :   rate,
        "description":  description
    })
    

def top_250_movies_title():
    movies_list = []

    for movie_item in MOVIE_ITEM_LIST:
        imdb_id = imdb_id_finder(movie_item)    #tt0068646
        title = title_finder(movie_item)
        poster = poster_finder(imdb_id)
        year = year_finder(movie_item)
        rank = rank_finder(movie_item)
        rate = rate_finder(movie_item)
        description = description_finder(movie_item)
        append_movies(movies_list, imdb_id, title, poster, year, rank, rate, description)
        print(f"added to list: {rank} {title}")
        
    #we got everything what we want in movies_list
    with open("./jsons/movies.json", "w", encoding="utf-8") as file:
        file.write(json.dumps(movies_list, indent=2))

    return movies_list

top_250_movies_title()