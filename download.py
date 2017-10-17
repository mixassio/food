import re
import requests
import bs4
import sqlite3

conn = sqlite3.connect('./food.db')
c = conn.cursor()
c.execute("DROP TABLE  foods_link")
c.execute("CREATE TABLE foods_link (link CHAR, title CHAR)")

list_foods = []
for page in range(1, 10):
    url = 'https://eda.ru/recepty?page={}'.format(page)
    foods_html = requests.get(url)
    soup = bs4.BeautifulSoup(foods_html.content, "lxml")
    for food in soup('h3', {'class': 'horizontal-tile__item-title item-title'}):
        print(food.a.span.string)
        print(food.a['href'])
        list_foods.append([food.a['href'], food.a.span.string])

for line in list_foods:
    c.execute("insert into foods_link values (?, ?)", line)
    conn.commit()
    print(line)