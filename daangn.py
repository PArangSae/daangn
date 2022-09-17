import requests
from bs4 import BeautifulSoup


class Daangn():

    def __init__(self):
        self.self = self

    def search(self, keyword):
        self.products = []
        webpage = requests.get(f"https://daangn.com/search/{keyword}")
        soup = BeautifulSoup(webpage.content, "html.parser")

        article_title = soup.find_all('span', 'article-title')
        article_price = soup.find_all('p', 'article-price')
        flea_market_article_link = soup.find_all('a',
                                                 'flea-market-article-link',
                                                 href=True)
        article_region_name = soup.find_all('p', 'article-region-name')

        for x in article_title:
            idx = article_title.index(x)
            self.products.append({
                "title":
                x.string,
                "price":
                article_price[idx].string,
                "region":
                article_region_name[idx].string,
                "id":
                flea_market_article_link[idx]["href"][10:]
            })
        return self.products

    def hot(self):
        self.products = []
        webpage = requests.get("https://daangn.com/hot_articles")
        soup = BeautifulSoup(webpage.content, "html.parser")

        card_title = soup.find_all('h2', 'card-title')
        card_price = soup.find_all('div', 'card-price')
        card_link = soup.find_all('a', 'card-link', href=True)
        card_region_name = soup.find_all('div', 'card-region-name')

        for x in card_title:
            idx = card_title.index(x)
            title = x.string
            price = card_price[idx].string.lstrip('\n').lstrip(' ').rstrip(
                ' ').rstrip('\n')
            region = card_region_name[idx].string.lstrip('\n').lstrip(
                ' ').rstrip(' ').rstrip('\n')
            id = card_link[idx]["href"][10:]
            self.products.append({
                "title": title,
                "price": price,
                "region": region,
                "id": id
            })
        return self.products
    
    def fetch_article(self, id):
        self.article = {}
        webpage = requests.get(f"https://daangn.com/articles/{id}")
        soup = BeautifulSoup(webpage.content, "html.parser")
        article_img = soup.find_all('img', "landscape")
        img = []
        for x in article_img:
            img.append(x["src"])
        user = {
            "nickname": soup.find_all('div', {'id': 'nickname'})[0].string,
            "region": soup.find_all('div', {"id": "region-name"})[0].string,
            "id": soup.find_all('a',
                                {'id': "article-profile-link"})[0]['href'][3:]
        }
        name = soup.find_all('h1', {'id': 'article-title'})[0].string
        price = int(
            float(soup.find_all('p', {'id': 'article-price'})[0]['content']))
        self.article = {'user': user, 'name': name, 'price': price}
        return self.article

    def fetch_user(self, id):
        self.user = {}
        webpage = requests.get(f"https://daangn.com/u/{id}")
        soup = BeautifulSoup(webpage.content, "html.parser")
        nickname = soup.find_all(
            "div", {'id': 'profile-image'})[0].findChildren('img')[0]['alt']
        print(nickname)
        articles = []
        card_link = soup.find_all('a', 'card-link')
        for x in card_link:
            articles.append(x['data-event-label'])
        self.user = {'articles': articles, 'nickname': nickname}
        return self.user
        
    # fetch things currently not working