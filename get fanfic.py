import time, os, scraper, requests, bs4, sqlite3, traceback, codecs


connection = sqlite3.connect('fanfiction.db')
c = connection.cursor()

c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='fanfiction' ''')

if c.fetchone()[0]==0:
    sql_command = ('''
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
        status INTEGER,
        story TEXT
    );''')

    c.execute(sql_command)
else:
    print('Table exists')

baseURL = str('http://fanfiction.net/s/')
ffscraper = scraper.Scraper()
x = 0

while True:
    print("Scraping Story Number:",x)
    c.execute('SELECT 1 FROM fanfiction WHERE id=? LIMIT 1', (x,))
    exists = c.fetchone()
    if exists == None:

        metadata = ffscraper.scrape_story_text(x, keep_html=False)

        if metadata == None:
            print("No story found at id",x)
            c.execute('''INSERT INTO fanfiction (id, canon_type, canon, authorid, title, updated, published, language, genre, rating, chapters, words, reviews, favs, follows, status, story)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (x, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None))
            connection.commit()
        else:
            fulltext = ''
            for y in range(0, len(metadata['chapters'].keys())):
                fulltext = fulltext + str(metadata['chapters'][y+1])

            fulltext = fulltext.replace("'",'"')

            c.execute('''INSERT INTO fanfiction (id, canon_type, canon, authorid, title, updated, published, language, genre, rating, chapters, words, reviews, favs, follows, status, story)
                            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', (metadata.get('id'), metadata.get('canon_type'), metadata.get('canon'), metadata.get('author_id'), metadata.get('title'), metadata.get('updated'), metadata.get('published'), metadata.get('lang'), " ".join(metadata.get('genres')), metadata.get('rated'), metadata.get('num_chapters'), metadata.get('num_words'), metadata.get('num_reviews'), metadata.get('num_favs'), metadata.get('num_follows'), metadata.get('status'), fulltext))
            print('Gathered metadata for id:',int(metadata.get('id')))

            connection.commit()
    
    else:
        print("Story with ID",x,"already exists in database, skipping.")
    x+=1

