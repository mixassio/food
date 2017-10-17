import requests
import bs4
import sqlite3


"""
conn = sqlite3.connect('./food.db')
c = conn.cursor()
#c.execute("DROP TABLE  recipies")
c.execute("CREATE TABLE recipies (page CHAR, link CHAR, title CHAR)")
"""

url = 'https://eda.ru/recepty/supy/klassicheskij-gaspacho-21178'

rec = requests.get(url)
soup = bs4.BeautifulSoup(rec.content, "lxml")

for ingridients in soup('p', {'class': 'ingredients-list__content-item content-item js-cart-ingredients'}):
    print(ingridients['data-ingredient-object'])