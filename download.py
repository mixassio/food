import requests
import bs4
import sqlite3

conn = sqlite3.connect('./food.db')
c = conn.cursor()
#c.execute("DROP TABLE  foods_link")
c.execute("CREATE TABLE foods_link (page CHAR, link CHAR, title CHAR)")

for page in range(1, 1000000):
    url = 'https://eda.ru/recepty?page={}'.format(page)
    foods_html = requests.get(url)
    soup = bs4.BeautifulSoup(foods_html.content, "lxml")
    for food in soup('h3', {'class': 'horizontal-tile__item-title item-title'}):
        c.execute("insert into foods_link values (?, ?, ?)", [page, food.a['href'], food.a.span.string])
    if page % 100 == 0:
        conn.commit()
        print(page)

