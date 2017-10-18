import re
import json
import requests
import bs4
import sqlite3



conn = sqlite3.connect('./food.db')
c = conn.cursor()
#c.execute("DROP TABLE  recipies")
#c.execute("CREATE TABLE recipies (id CHAR, name CHAR, type CHAR, portions CHAR, time CHAR, link CHAR, imageUrl CHAR)")


url = 'https://eda.ru/recepty/supy/krem-sup-iz-tikvi-16754'
rec = requests.get(url)
soup = bs4.BeautifulSoup(rec.content, "lxml")

for ingridients in soup('p', {'class': 'ingredients-list__content-item content-item js-cart-ingredients'}):
    print(ingridients['data-ingredient-object'])

print(soup('button', {'class': 'cart__buy-button js-cart-buy-button'})[0]['data-recipe-object'])

for step in soup('span', {'instruction__description'}):
    print(step.text)





list_links = c.execute('select link from foods_link').fetchall()
m1 = map(lambda x: x[0].split('/'), list_links)
m2 = map(lambda x: ['https://eda.ru', x[1], x[2], x[3]], m1)

for i in m2:
    url = '/'.join(i)
    rec = requests.get(url)
    soup = bs4.BeautifulSoup(rec.content, "lxml")
    try:
        time = soup('div', {'class': 'instruction-controls'})[0].text
    except IndexError:
        time = None
    print(url)
    data_rec = soup('button', {'class': 'cart__buy-button js-cart-buy-button'})[0]['data-recipe-object']
    obj = json.loads(data_rec)
    # Общие данные о рецепте
    print([obj['id'], obj['name'], i[2], obj['portions'], time, url, re.findall('(s\d.*)', obj['imageUrl'])[0]])
    ingridients = soup('p', {'class': 'ingredients-list__content-item content-item js-cart-ingredients'})
    for ingridient in ingridients:
        ingr = json.loads(ingridient['data-ingredient-object'])
        print([obj['id'], ingr['id'], ingr['name'], ingr['amount']])
    for step in soup('span', {'instruction__description'}):
        print(step.text)


"""
Поиск тегов не доделан, но возможен и нужен
for tag in soup('div', {'class': 'recipe__title'}):
    print('___------____')
    print(tag)
    for i in tag.ul:
        print(type(i))
        #print(i.li)
"""

