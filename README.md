# Fanfiction-Scraper-V2
Scrapes fanfictions, except better then the original one.

x value in get_fanfic.py determines what story ID the scraper starts at.
The scraper will resume where it left off when restarted, as long as the database is still in place.
This process of catching up is slow and probably horribly inefficient, so sometimes increasing the x value manually may speed up the process.

The scraper relies on sqlite3, beautifulsoup4, and the fanfic library that I butchered. https://github.com/lonewolf316/fanfiction