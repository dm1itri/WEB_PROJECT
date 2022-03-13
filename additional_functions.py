from requests import get
from bs4 import BeautifulSoup


def parse_news():
    url = 'https://www.rbc.ru/technology_and_media/?utm_source=topline'
    response = get(url)
    soup = BeautifulSoup(response.text)
    quotes1 = soup.find_all('span', class_='item__title', limit=11)
    quotes2 = soup.find_all('span', class_='item__category', limit=11)
    quotes_img = soup.find_all('img', class_='g-image item__image')
    quotes3 = soup.find_all('div', class_='item__wrap', limit=11)

    sp = []
    for i in range(11):
        sp.append((quotes1[i].text.strip(), quotes2[i].text.strip()))
    for i in range(11):
        if 'img' not in [j.name for j in quotes3[i].descendants]:
            sp[i] = (sp[i][0], sp[i][1], False)
        else:
            sp[i] = (sp[i][0], sp[i][1], quotes_img[0]['srcset'])
            quotes_img.remove(quotes_img[0])
    return sp
