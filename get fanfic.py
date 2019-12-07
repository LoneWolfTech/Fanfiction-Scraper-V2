import time, os, fanfiction, requests, bs4, sqlite3


connection = sqlite3.connect("fanfiction.db")
c = connection.cursor()

c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='fanfiction' ''')

if c.fetchone()[0]==0:
    sql_command = ("""
    CREATE TABLE fanfiction (
        id INTEGER PRIMARY KEY,
        canon_type TEXT,
        canon TEXT,
        authorid INTEGER,
        title TEXT,
        updated INTEGER,
        published INTEGER,
        language TEXT,
        genre TEXT,
        rating TEXT,
        chapters INTEGER,
        words INTEGER,
        reviews INTEGER,
        favs INTEGER,
        follows INTEGER,
        status INTEGER
    );""")

    c.execute(sql_command)
else:
    print("Table exists")

baseURL = str("http://fanfiction.net/")

scraper = fanfiction.Scraper()
metadata = scraper.scrape_story_metadata()
 
entry_str="""INSERT INTO fanfiction (id, canon_type, canon, authorid, title, updated, published, language, genre, rating, chapters, words, reviews, favs, follows, status)
            VALUES ("{id}", "{canon_type}", "{canon}", "{authorid}", "{title}", "{updated}", "{published}", "{language}", "{genre}", "{rating}", "{chapters}", "{words}", "{reviews}", "{favs}", "{follows}", "{status}");"""
print(int(metadata.get('id')))
entry_command = entry_str.format(id = metadata.get('id'), canon_type = metadata.get('canon_type'), canon = metadata.get('canon'), authorid = metadata.get('author_id'), title = metadata.get('title'), updated = metadata.get('updated'), published = metadata.get('published'), language = metadata.get('lang'), genre = metadata.get('genres'), rating = metadata.get('rated'), chapters = metadata.get('num_chapters'), words = metadata.get('num_words'), reviews = metadata.get('num_reviews'), favs = metadata.get('num_favs'), follows = metadata.get('num_follows'), status = metadata.get('status'))
c.execute(entry_command)
print(metadata)
connection.commit()