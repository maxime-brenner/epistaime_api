import spacy
import requests
import re

nlp = spacy.load("fr_core_news_md")

import fr_core_news_md

def bfmtv_clean_url_title(url: str):
    url = re.sub(r"_(\w)+-(\d)+.html","", url)
    url = re.sub(r"https://.+/", "", url)
    url = re.sub("-", " ", url)

    return url

nlp = fr_core_news_md.load()

articles = requests.get('http://localhost:8000/api/scraper/retrieve/bfmtv/').json()["articles"]
trends = requests.get('http://localhost:8000/api/scraper/trends/').json()["trends"]

for trend in trends:
    print(trend)

print("Début de la recherche de similarité")
for article in articles[:20]:
    article["url"]
    clean_url = bfmtv_clean_url_title(article["url"])
    clean_url = nlp(clean_url)
    tab = [w for w in clean_url if w.pos_ in ["NOUN", "VERB"]]
    for word in tab:
        for trend in trends:
            if word.similarity(nlp(trend)) > 0.3:
                print(word.similarity(nlp(trend)), word, trend)
print("Fin de la recherche")

doc = nlp('Le retour au bercail')
search = nlp('maison')

""" nouns = [w for w in doc if w.pos_ in  ["NOUN", "VERB"]]

for w in nouns:
    print(w.similarity(search), w) """