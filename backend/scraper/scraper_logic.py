from bs4 import BeautifulSoup as bs
import requests
from scraper.models import StreamModel, ArticleScraperModel, CategoryArticle
import json
import re

def futura():
    url="https://www.futura-sciences.com/sciences/actualites/"
    domain="https://www.futura-sciences.com"
    html=requests.get(url).content


    soup=bs(html, 'html.parser')

    articles=soup.find_all("a", attrs={"class":"article-card-box"})

    for article in articles:
        print(article.find("p", attrs={"class": "article-card-title"}).get_text(), domain+article["href"])

def extract_article(bs_object:str, domain:str):
    titre:str = bs_object.find("a")["title"]
    time: str = bs_object.find("time", attrs={"class":"content_live_time"}).get_text().replace(":","")
    category: str = bs_object.find("span", attrs={"class":"block_category"}).get_text()
    url: str = domain+bs_object.find("a")["href"]
    article_id: str = time+category[0:2]+titre.replace(" ","")[0:2]
    newArticle = {'article_id':article_id, 'titre':titre, 'time':'{:0>4}'.format(time), 'category':category, 'posted':False, 'url':url}
    return newArticle

def bfmtv_clean_url_title(url: str):
    url = re.sub(r"_(\w)+-(\d)+.html","", url)
    url = re.sub(r"https://.+/", "", url)
    url = re.sub("-", " ", url)

def create_article(article):
    ArticleScraperModel.objects.create(**article)

def get_categories():
    req = CategoryArticle.objects.all()
    cat_tab = [cat.name for cat in req]
    return cat_tab

def create_categories(cat: str, brand: str):
    CategoryArticle.objects.create(name=cat, brand_name=brand)

def check_categories(tab: [str], cat: str, brand: str):
    if cat not in tab:
        create_categories(cat, brand)
        tab=get_categories()
        return tab
    else:
        return tab
    

def check_time_format(time):
    try:
        int(time)
        return True
    except ValueError:
        return False
        
def retrieve_time(obj):
    return obj["time"]

def bfmtv():
    url="https://www.bfmtv.com/news-24-7/"
    html=requests.get(url).content
    domain="https://www.bfmtv.com/news-24-7"

    soup=bs(html, "html.parser")

    articles=soup.find_all("article", attrs={"class":"content_live_block"})
    
    bfmtv_stream=ArticleScraperModel.objects.all().order_by("-time")

    cat = get_categories()

    if len(bfmtv_stream)>0:
        print("Mise à jour")
        balise=int(bfmtv_stream[0].time)
        print(balise)
        for article in articles:
            art=extract_article(article, domain)
            if check_time_format(art["time"])==True and int(art["time"])>balise:
                create_article(art)
                cat = check_categories(cat, art["category"], "bfmtv")
            else:
                break
    elif len(bfmtv_stream)==0:
        print("Création des articles de la journée")
        for article in articles:
            art=extract_article(article, domain)
            if check_time_format(art["time"]):
                create_article(art)
                cat = check_categories(cat, art["category"], "bfmtv")
            else: 
                break

def trends24():
    url = "https://trends24.in/france/"
    html = requests.get(url).content

    soup = bs(html, "html.parser")

    trends = soup.find("ol", attrs={"class":"trend-card__list"}).find_all("li")
    res = [re.sub(r"#|(\d)+K", "", trend.get_text()) for trend in trends]

    print(res)

    return res

def links_from_google_search(search:str, number:int=30):
    cookies = {"CONSENT":"PENDING+748", "SOCS":"CAISNQgCEitib3FfaWRlbnRpdHlmcm9udGVuZHVpc2VydmVyXzIwMjMxMjA1LjA1X3AyGgJmciAEGgYIgP_TqwY"}
    url = f"https://www.google.com/search?q={search}&tbm=nws&lr=lang_fr&num=10"
    print(url)
    res = requests.get(url, cookies=cookies)
    """ soup = bs(res.content, 'html.parser')
    glinks = soup.find_all("a")
    print(glinks)
    to_follow=[l["href"] for l in glinks if re.match(r"https:\/\/consent.google.com/dl\?continue=",l["href"])]
    to_follow_obj=[l for l in glinks if re.match(r"https:\/\/consent.google.com/dl\?continue=",l["href"])]
    followed = to_follow_obj[0].get('href', None)
    flink = to_follow[0]
    print(glinks, res.request.headers)
    flink=re.sub(r"https:\/\/consent.google.com/d\?continue=", "", flink)
    flink = re.sub(r"%3D", "=", flink)
    flink = re.sub(r"%26", "&", flink)

    res = requests.get(followed, headers=headers, allow_redirects=False) """
    soup = bs(res.content, 'html.parser')
    articles = soup.find_all("a")

    print(res.request.headers, res.history, res.url)

    """ with open('result.html', 'w') as res:
        res.write(soup.text) """
    links = [re.sub(r'\/url\?q=','',article["href"]) for article in articles if re.match(r'\/url\?q=', article["href"])!= None] 
    links = [link for link in links if re.match(r'https:\/\/maps.google.com', link)==None]
    links = [link for link in links if re.match(r'https:\/\/(\w)+.google.com', link)==None]
    links = [link for link in links if re.match(r'^https', link)!=None]


    return links

