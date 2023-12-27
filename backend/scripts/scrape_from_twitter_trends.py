import requests
import re
import time

domain_name='http://localhost:8000/'

trends_url = domain_name+"api/scraper/trends/"
google_search_url = domain_name+"api/scraper/google/search/news/"
generator_url = domain_name+"api/generator/"
tweet_url = domain_name+"api/twitter/"
post_url = domain_name+"api/post/"

results = {}

def get_source(url:str):
    source:str = re.match(r"https:\/\/www.(\w)+.(\w)+", url).group()
    source:str = re.sub(r"https:\/\/www.", "", source)

    return source

print("Recherche des tendances")
trends = requests.get(trends_url).json()['trends']

for trend in trends[:5]:
    try: 
        print(f"Recherche d'articles pour le mot {trend}")
        res = requests.post(google_search_url, {"search":trend}).json()["links"]
        print(res[0])
        articles = [article for article in res if re.match(r"^https:\/\/(\w)+.google.com", article)==None]
        results[trend]=articles
    except:
        pass

for keys in results.keys():
    print(f"Génération d'un tweet pour le mot {keys}")
    try:
        article = results[keys][0]
        try:
            source = get_source(article)
        except:
            source=""
        res_generate=requests.post(generator_url, {"article_url":article})
        generated_text=res_generate.json()["message"]
        content_raw='\U0001F4F0'+'Actualité'+'\n'+generated_text+"(source "+source+")"+'\n'+article
        add_generated_text=requests.post(post_url, {"account":"EPM", "content_raw":content_raw, "generated_text":generated_text, "isPosted":True})
        res_tweet=requests.post(tweet_url, {"id":add_generated_text.json()["id"], "account":"EPM"})
        time.sleep(30)
    except:
        pass
    
    



