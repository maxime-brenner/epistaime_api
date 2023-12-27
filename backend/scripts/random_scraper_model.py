import requests
import json
from random import randint

domain='http://localhost:8000/'
""" http://ec2-35-181-191-107.eu-west-3.compute.amazonaws.com/ """
url_all=domain+'api/streamarticle/'
url_create_post=domain+'api/post/'
url_generate=domain+'api/generator/'
url_tweet=domain+'api/twitter/'

print("Recherche des articles")
res_get = requests.get(url_all)
all:list = res_get.json()

print("Choix d'un article")
to_post_index=randint(0, len(all)-1)
article_to_post=all[to_post_index]
print(article_to_post["url"])

print("Génération du texte")
res_generate=requests.post(url_generate, {"article_url":article_to_post["url"]})
print(res_generate.content)
generated_text=res_generate.json()["message"]
print(res_generate.json()["message"])

print("Création du texte à poster")
content_raw='\U0001F4F0'+'Actualité'+'\n'+generated_text+"(source BFMTV)"+'\n'+article_to_post["url"]
category = article_to_post["category"]

print("Création du post")
add_generated_text=requests.post(url_create_post, {"account":"INFO", "content_raw":content_raw, "generated_text":generated_text, "isPosted":True, "category": category})
print(add_generated_text.status_code)

print("Création du tweet")
res_tweet=requests.post(url_tweet, {"id":add_generated_text.json()["id"], "account":"INFO"})

print("Tweet envoyé")
print("Mise à jour de l'article du scraper")
requests.put(url_all+str(to_post_index)+"/", {"posted":True})

print(to_post_index)